EXPIRED_SIGNATURE_ERROR = 'failed to authenticate due to an expired access token'
JWT_CLAIMS_ERROR = 'failed to authenticate due to failing claim checks'
JWT_ERROR = 'failed to authenticate due to a malformed access token'
REFRESH_TOKEN_ERROR = 'URL is unreachable or refresh_token has expired or invalid token'
REMOTE_REFRESH_TOKEN_ERROR = 'URL is unreachable or access restriction or access_token has expired or invalid token'

OBJ_ID_NOT_FOUND = 'There is no object with id:'
OIDC_PROFILE_NOT_FOUND = 'There is no user profile with sub:'


def list_id_to_str(id_data) -> str:
    if type(id_data) not in (list, set, tuple):
        return id_data

    return ", ".join(str(id_obj) for id_obj in id_data)


def get_backend_message(backend, message):
    return f"{backend}: {message}"


def get_backend_message_with_error(backend, message, error):
    return f"{backend}: {message}: {error}"


def obj_id_not_found(obj_id, message=OBJ_ID_NOT_FOUND):
    return f"{message} {list_id_to_str(obj_id)}"
