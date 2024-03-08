from wykop_sdk_reloaded.exceptions import WykopApiError

from . import _urls
from ._request import ApiRequester


class AuthClient:
    def __init__(self):
        self.key = None
        self.secret = None
        self.jwt_app_token = None
        self.jwt_user_token = None
        self.jwt_refresh_user_token = None

    def __generate_jwt_user_token(self) -> str:
        return ApiRequester(url=_urls.AUTH_URL, token=None).post(
            data={"key": self.key, "secret": self.secret}
        )["data"]["token"]
    
    def check_authentication(self):
        if not self.jwt_app_token and not self.jwt_user_token:
            raise WykopApiError("Wymagana autentykacja. Wywołaj AuthClient.authenticate_app() albo AuthClient.authenticate_user()")
    
    def wykop_connect(self):
        print(ApiRequester(url=_urls.CONNECT_URL, token=self.jwt_app_token).get()["data"]["connect_url"])

    def authenticate_app(self, key: str, secret: str):
        self.key = key
        self.secret = secret

        self.jwt_app_token = self.__generate_jwt_user_token()

    def authenticate_user(self, token: str, refresh_token: str):
        self.jwt_user_token = token
        self.jwt_refresh_user_token = refresh_token

    def get_jwt_token(self):
        """
        Wybiera bardziej sprawczy token
        """
        return self.jwt_user_token if self.jwt_user_token else self.jwt_app_token
