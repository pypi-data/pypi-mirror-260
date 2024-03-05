import requests

from metastock.modules.core.util.app_error import AppError


class HttpClient:
    instance = None

    @staticmethod
    def get(url, config=None):
        if config is None:
            config = {}
        response = requests.get(url)

        return response

    @staticmethod
    def post(url, data: dict, config: dict = None, raise_for_status=False):
        response = requests.post(url, json=data)

        if raise_for_status is True:
            response.raise_for_status()

        return response

    @staticmethod
    def patch(url, data: dict, config: dict = None, raise_for_status=False):
        response = requests.patch(url, json=data)

        if raise_for_status is True:
            response.raise_for_status()

        return response

    def fetch(self, url: str):
        res = self.get(url)
        if res.status_code != 200:
            raise AppError("Due to error get tick history data")

        return res.json()


def http_client() -> HttpClient:
    if HttpClient.instance is None:
        HttpClient.instance = HttpClient()
    return HttpClient.instance
