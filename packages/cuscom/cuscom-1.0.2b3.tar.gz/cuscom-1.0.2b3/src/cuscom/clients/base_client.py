import logging
from posixpath import join as join_url

import requests

from cuscom.utils import from_kebab_case_key

log = logging.getLogger(__name__)


class ClientException(Exception):
    def __init__(self, status_code, body, url, message=None):
        super().__init__(message or f"Failure using request client [{status_code}]: {body}")
        self.status_code = status_code
        self.body = body
        self.url = url

    @classmethod
    def from_response(cls, response, url):
        return cls(response.status_code, response.text, url)

    def __repr__(self):
        return f"<{self.__class__.__name__}({self.status_code, self.body})>"


class Client:
    def __init__(self, base_url):
        self._base_url = base_url

    def request(self, endpoint, method, **kwargs):
        url = join_url(self._base_url, endpoint)
        response = requests.api.request(method=method, url=url, **kwargs)

        if response.status_code not in [200]:
            raise ClientException.from_response(response, url)

        return response.json(object_hook=from_kebab_case_key)

    def __repr__(self):
        return f"<{self.__class__.__name__}({self._base_url})>"
