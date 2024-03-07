from .http import HttpClient
from .mail import MailParams
from .errors import ESTRHourlyLimitReachedError, ESTRForbiddenError, ESTRError

API_URL = 'https://api.envialosimple.email/api/v1'


class Mail():

    ENDPOINT = '/mail/send'

    def __init__(self, httpClient: HttpClient) -> None:
        self._http = httpClient

    def send(self, mail_params: MailParams) -> dict:
        http_code, response = self._http.post(
            API_URL + self.ENDPOINT, mail_params.to_dict())

        if http_code >= 400:
            if http_code == 429:
                raise ESTRHourlyLimitReachedError(
                    'Hourly limit reached. Please try again later.')
            elif http_code == 403:
                raise ESTRForbiddenError(
                    'Make sure API Key is correct and not disabled')
            else:
                raise ESTRError(
                    f'The server responded with code {http_code}')

        return response
