from rest_framework import permissions


def UserPermission(*user_group):
    """
    :param user_group: List of user groups
    """

    class Permission(permissions.BasePermission):
        def has_permission(self, request, view):
            if not user_group:
                return True

            if not request.user.is_authenticated:
                if None in user_group:
                    return True

                return False

            decoded_token = request.user.oidc_profile.jwt
            token_user_group = decoded_token.get('user_group')
            intersection = [item for item in token_user_group if item in user_group]

            return len(intersection) != 0

    return Permission
