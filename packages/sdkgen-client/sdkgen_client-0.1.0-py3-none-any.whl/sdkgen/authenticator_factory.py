from .authenticator import HttpBasicAuthenticator, HttpBearerAuthenticator, ApiKeyAuthenticator, \
    OAuth2Authenticator, AnonymousAuthenticator
from .credentials import CredentialsInterface, HttpBasic, HttpBearer, ApiKey, OAuth2, Anonymous
from .exceptions import InvalidCredentialsException


class AuthenticatorFactory:
    @staticmethod
    def factory(credentials: CredentialsInterface):
        if isinstance(credentials, HttpBasic):
            return HttpBasicAuthenticator(credentials)
        elif isinstance(credentials, HttpBearer):
            return HttpBearerAuthenticator(credentials)
        elif isinstance(credentials, ApiKey):
            return ApiKeyAuthenticator(credentials)
        elif isinstance(credentials, OAuth2):
            return OAuth2Authenticator(credentials)
        elif isinstance(credentials, Anonymous):
            return AnonymousAuthenticator(credentials)
        else:
            raise InvalidCredentialsException("Could not find authenticator for credentials")
        pass
