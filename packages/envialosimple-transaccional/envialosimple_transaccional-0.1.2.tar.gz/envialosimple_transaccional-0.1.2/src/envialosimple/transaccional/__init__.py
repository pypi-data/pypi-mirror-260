
from .http import HttpClient
from .endpoints import Mail


class Transaccional():

    def __init__(self, api_key: str) -> None:
        self.httpClient = HttpClient(api_key)
        self.mail = Mail(self.httpClient)
