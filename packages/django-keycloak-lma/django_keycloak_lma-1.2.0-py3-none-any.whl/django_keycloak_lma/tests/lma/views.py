"""
from django_keycloak_lma.auth.permissions import UserPermission
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes, parser_classes, authentication_classes, \
    permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import logout as django_logout

from django_keycloak_lma import serializers as keycloak_serializers
from django_keycloak_lma.auth.backends import KeycloakPasswordAuthentication, KeycloakTokenAuthentication
from django_keycloak_lma.services import oidc_profile, remote_client

from . import serializers
from .choices import UserGroup


@api_view(['POST'])
@renderer_classes([JSONRenderer])
@parser_classes([JSONParser])
@authentication_classes([KeycloakPasswordAuthentication])
def login(request):
    if not hasattr(request, 'auth'):
        raise Exception("Section 'auth' was not found")

    auth_data = keycloak_serializers.TokenSerializer(request.auth).data

    return Response(auth_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@renderer_classes([JSONRenderer])
@parser_classes([JSONParser])
@authentication_classes([KeycloakTokenAuthentication])
@permission_classes((UserPermission(UserGroup.EXCHANGE),))
def check_access(request):

    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@renderer_classes([JSONRenderer])
@parser_classes([JSONParser])
def refresh_token(request):
    if not hasattr(request, 'realm'):
        raise ImproperlyConfigured('Add BaseKeycloakMiddleware to middlewares')

    serializer = serializers.RefreshTokenSerializer(data=request.data)
    if not serializer.is_valid():
        raise Exception(serializer.errors)

    profile = oidc_profile.refresh_token(request.realm.client, serializer.validated_data["refresh"])
    auth_data = keycloak_serializers.TokenSerializer(profile).data

    return Response(auth_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@renderer_classes([JSONRenderer])
@parser_classes([JSONParser])
def exchange_remote_token(request):
    if not hasattr(request, 'realm'):
        raise ImproperlyConfigured('Add BaseKeycloakMiddleware to middlewares')

    serializer = serializers.AccessTokenSerializer(data=request.data)
    if not serializer.is_valid():
        raise Exception(serializer.errors)

    profile = remote_client.exchange_remote_token(request.realm.client, serializer.validated_data["access"])
    auth_data = keycloak_serializers.TokenSerializer(profile).data

    return Response(auth_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@renderer_classes([JSONRenderer])
@parser_classes([JSONParser])
@authentication_classes([KeycloakTokenAuthentication])
def logout(request):
    if not hasattr(request, 'auth'):
        raise Exception("Section 'auth' was not found")

    oidc_profile.logout(request.user.oidc_profile)
    django_logout(request)

    return Response(status=status.HTTP_200_OK)

"""
