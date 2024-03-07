import requests


class HttpClient():

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def post(self, url: str, data: dict) -> tuple:

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.api_key
        }

        response = requests.post(url, json=data, headers=headers)

        http_code = response.status_code

        json_response = response.json()

        if http_code == 500:
            raise ValueError(f'The server responded with code {http_code}')

        if type(json_response) is not dict:
            raise ValueError('The server did not respond with JSON')

        return (http_code, json_response)
