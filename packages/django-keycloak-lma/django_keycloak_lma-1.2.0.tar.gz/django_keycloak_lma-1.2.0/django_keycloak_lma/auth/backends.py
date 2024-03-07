import logging
from typing import Set
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.utils import timezone
from jose.exceptions import (
    ExpiredSignatureError,
    JWTClaimsError,
    JWTError,
)
from keycloak.exceptions import KeycloakClientError
from rest_framework.authentication import BasicAuthentication
from rest_framework import HTTP_HEADER_ENCODING
import django_keycloak_lma.services.oidc_profile
import django_keycloak_lma.services.messages as messages

AUTH_HEADER_TYPES = ('Bearer',)

if not isinstance(AUTH_HEADER_TYPES, (list, tuple)):
    AUTH_HEADER_TYPES = (AUTH_HEADER_TYPES,)

AUTH_HEADER_TYPE_BYTES: Set[bytes] = {
    h.encode(HTTP_HEADER_ENCODING) for h in AUTH_HEADER_TYPES
}

logger = logging.getLogger(__name__)


class KeycloakAuthorizationBase(object):

    def get_user(self, user_id):
        UserModel = get_user_model()

        try:
            user = UserModel.objects.select_related('oidc_profile__realm').get(
                pk=user_id)
        except UserModel.DoesNotExist:
            return None

        if user.oidc_profile.refresh_expires_before > timezone.now():
            return user

        return None

    def get_all_permissions(self, user_obj, obj=None):
        if not user_obj.is_active or user_obj.is_anonymous or obj is not None:
            return set()
        if not hasattr(user_obj, '_keycloak_perm_cache'):
            user_obj._keycloak_perm_cache = self.get_keycloak_permissions(
                user_obj=user_obj)
        return user_obj._keycloak_perm_cache

    def get_keycloak_permissions(self, user_obj):
        if not hasattr(user_obj, 'oidc_profile'):
            return set()

        rpt_decoded = django_keycloak_lma.services.oidc_profile\
            .get_entitlement(oidc_profile=user_obj.oidc_profile)

        if settings.KEYCLOAK_PERMISSIONS_METHOD == 'role':
            return [
                role for role in rpt_decoded['resource_access'].get(
                    user_obj.oidc_profile.realm.client.client_id,
                    {'roles': []}
                )['roles']
            ]
        elif settings.KEYCLOAK_PERMISSIONS_METHOD == 'resource':
            permissions = []
            for p in rpt_decoded['authorization'].get('permissions', []):
                if 'scopes' in p:
                    for scope in p['scopes']:
                        if '.' in p['resource_set_name']:
                            app, model = p['resource_set_name'].split('.', 1)
                            permissions.append('{app}.{scope}_{model}'.format(
                                app=app,
                                scope=scope,
                                model=model
                            ))
                        else:
                            permissions.append('{scope}_{resource}'.format(
                                scope=scope,
                                resource=p['resource_set_name']
                            ))
                else:
                    permissions.append(p['resource_set_name'])

            return permissions
        else:
            raise ImproperlyConfigured(
                'Unsupported permission method configured for '
                'Keycloak: {}'.format(settings.KEYCLOAK_PERMISSIONS_METHOD)
            )

    def has_perm(self, user_obj, perm, obj=None):

        if not user_obj.is_active:
            return False

        granted_perms = self.get_all_permissions(user_obj, obj)
        return perm in granted_perms


class KeycloakPasswordAuthentication(BasicAuthentication, KeycloakAuthorizationBase):
    def auth(self, request, username, password, user):

        if not hasattr(request, 'realm'):
            raise ImproperlyConfigured(
                'Add BaseKeycloakMiddleware to middlewares')

        if not request.realm:
            # If request.realm does exist, but it is filled with None, we
            # can't authenticate using Keycloak
            return None

        try:
            keycloak_openid_profile = django_keycloak_lma.services\
                .oidc_profile.update_or_create_from_password_credentials(
                    client=request.realm.client,
                    username=username,
                    password=password,
                    user=user
                )
        except KeycloakClientError:
            logger.debug('KeycloakPasswordAuthentication: failed to '
                         'authenticate.')
        else:
            return keycloak_openid_profile.user, keycloak_openid_profile

        return None

    def authenticate_credentials(self, userid, password, request=None):
        # Base auth:
        user, _ = super().authenticate_credentials(userid, password, request)
        # keycloak-auth:
        user, token = self.auth(request, userid, password, user)

        return user, token


class KeycloakAuthorizationCodeBackend(KeycloakAuthorizationBase):

    def authenticate(self, request, code, redirect_uri):

        if not hasattr(request, 'realm'):
            raise ImproperlyConfigured(
                'Add BaseKeycloakMiddleware to middlewares')

        keycloak_openid_profile = django_keycloak_lma.services\
            .oidc_profile.update_or_create_from_code(
                client=request.realm.client,
                code=code,
                redirect_uri=redirect_uri
            )

        return keycloak_openid_profile.user


class KeycloakPasswordCredentialsBackend(KeycloakAuthorizationBase):

    def authenticate(self, request, username, password):

        if not hasattr(request, 'realm'):
            raise ImproperlyConfigured(
                'Add BaseKeycloakMiddleware to middlewares')

        if not request.realm:
            # If request.realm does exist, but it is filled with None, we
            # can't authenticate using Keycloak
            return None

        try:
            keycloak_openid_profile = django_keycloak_lma.services\
                .oidc_profile.update_or_create_from_password_credentials(
                    client=request.realm.client,
                    username=username,
                    password=password
                )
        except KeycloakClientError:
            logger.debug('KeycloakPasswordCredentialsBackend: failed to '
                         'authenticate.')
        else:
            return keycloak_openid_profile.user

        return None


class KeycloakIDTokenAuthorizationBackend(KeycloakAuthorizationBase):

    def authenticate(self, request, access_token):

        if not hasattr(request, 'realm'):
            raise ImproperlyConfigured(
                'Add BaseKeycloakMiddleware to middlewares')

        try:
            oidc_profile = django_keycloak_lma.services.oidc_profile\
                .get_or_create_from_id_token(
                    client=request.realm.client,
                    id_token=access_token
                )
        except ExpiredSignatureError:
            # If the signature has expired.
            logger.debug('KeycloakBearerAuthorizationBackend: failed to '
                         'authenticate due to an expired access token.')
        except JWTClaimsError as e:
            logger.debug('KeycloakBearerAuthorizationBackend: failed to '
                         'authenticate due to failing claim checks: "%s"'
                         % str(e))
        except JWTError:
            # The signature is invalid in any way.
            logger.debug('KeycloakBearerAuthorizationBackend: failed to '
                         'authenticate due to a malformed access token.')
        else:
            return oidc_profile.user

        return None


class KeycloakTokenAuthentication(KeycloakAuthorizationBase):
    www_authenticate_realm = "api"
    media_type = "application/json"
    header_key = "HTTP_AUTHORIZATION"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.user_model = get_user_model()

    def authenticate(self, request):

        if not hasattr(request, 'realm'):
            raise ImproperlyConfigured('Add BaseKeycloakMiddleware to middlewares')

        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        oidc_profile = self.get_profile(request, raw_token)

        return oidc_profile.user, oidc_profile

    def authenticate_header(self, request):
        return '{} realm="{}"'.format(
            AUTH_HEADER_TYPES[0],
            self.www_authenticate_realm,
        )

    def get_header(self, request):
        """
        Extracts the header containing the JSON web token from the given
        request.
        """
        header = request.META.get(self.header_key)

        if isinstance(header, str):
            # Work around django test client oddness
            header = header.encode(HTTP_HEADER_ENCODING)

        return header

    def get_raw_token(self, header):
        """
        Extracts an unvalidated JSON web token from the given "Authorization"
        header value.
        """
        parts = header.split()

        if len(parts) == 0:
            # Empty AUTHORIZATION header sent
            return None

        if parts[0] not in AUTH_HEADER_TYPE_BYTES:
            # Assume the header does not contain a JSON web token
            return None

        if len(parts) != 2:
            raise KeycloakClientError(
                _("Authorization header must contain two space-delimited values"),
                code="bad_authorization_header",
            )

        return parts[1]

    def get_profile(self, request, access_token):
        try:
            oidc_profile = django_keycloak_lma.services.oidc_profile\
                .get_from_id_token(
                    client=request.realm.client,
                    id_token=access_token
                )
            initiate_time = timezone.now()
            if oidc_profile.expires_before is None or initiate_time > oidc_profile.expires_before:
                raise ExpiredSignatureError()
        except ExpiredSignatureError:
            # If the signature has expired.
            message = messages.get_backend_message('KeycloakTokenAuthentication', messages.EXPIRED_SIGNATURE_ERROR)
            logger.debug(message)
            raise ExpiredSignatureError(message)
        except JWTClaimsError as ex:
            message = messages.get_backend_message_with_error('KeycloakTokenAuthentication', messages.JWT_CLAIMS_ERROR, str(ex))
            logger.debug(message)
            raise JWTClaimsError(message)
        except JWTError:
            # The signature is invalid in any way.
            message = messages.get_backend_message('KeycloakTokenAuthentication', messages.JWT_ERROR)
            logger.debug(message)
            raise JWTError(message)

        return oidc_profile
