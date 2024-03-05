import base64

from requests.auth import AuthBase

from .credentials import HttpBasic, HttpBearer, ApiKey, OAuth2, Anonymous


class AuthenticatorInterface(AuthBase):
    pass


class AnonymousAuthenticator(AuthenticatorInterface):
    def __init__(self, credentials: Anonymous):
        self.credentials = credentials

    def __call__(self, request):
        return request
        pass


class HttpBasicAuthenticator(AuthenticatorInterface):
    def __init__(self, credentials: HttpBasic):
        self.credentials = credentials

    def __call__(self, request):
        request.headers["Authorization"] = "Basic " + str(
            base64.b64encode(self.credentials.username + ":" + self.credentials.password))
        return request
        pass


class HttpBearerAuthenticator(AuthenticatorInterface):
    def __init__(self, credentials: HttpBearer):
        self.credentials = credentials

    def __call__(self, request):
        request.headers["Authorization"] = "Bearer " + self.credentials.token
        return request
        pass


class ApiKeyAuthenticator(AuthenticatorInterface):
    def __init__(self, credentials: ApiKey):
        self.credentials = credentials

    def __call__(self, request):
        request.headers[self.credentials.name] = self.credentials.token
        return request
        pass


class OAuth2Authenticator(AuthenticatorInterface):
    def __init__(self, credentials: OAuth2):
        self.credentials = credentials

    def __call__(self, request):
        request.headers["Authorization"] = "Bearer " + self.get_access_token()
        return request
        pass

    def get_access_token(self) -> str:
        return ""
