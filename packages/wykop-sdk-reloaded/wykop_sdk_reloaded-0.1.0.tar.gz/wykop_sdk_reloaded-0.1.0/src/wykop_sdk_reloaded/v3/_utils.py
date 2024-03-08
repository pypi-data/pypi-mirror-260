import functools

from wykop_sdk_reloaded.exceptions import WykopApiError

def auth_user_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]

        if not self.auth.jwt_user_token or not self.auth.jwt_refresh_user_token:
            raise WykopApiError("JWT user token must be set, use AuthClient(...).wykop_connect() to get it.")

        return func(*args, **kwargs)
    return wrapper
