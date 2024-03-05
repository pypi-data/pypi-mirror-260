from .access_token import AccessToken


class TokenStoreInterface:
    def get(self) -> AccessToken:
        pass

    def persist(self, token: AccessToken):
        pass

    def remove(self):
        pass

    pass


class MemoryTokenStore(TokenStoreInterface):
    def __init__(self):
        self.token = None

    def get(self) -> AccessToken:
        return self.token
        pass

    def persist(self, token: AccessToken):
        self.token = token
        pass

    def remove(self):
        self.token = None
        pass

    pass
