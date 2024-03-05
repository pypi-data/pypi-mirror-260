from .._auth_client import AuthenticatedClient


class BaseResource:
    def __init__(self, *, client: AuthenticatedClient):
        self.client = client
