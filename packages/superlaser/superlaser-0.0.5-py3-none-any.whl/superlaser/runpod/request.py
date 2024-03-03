import os
import requests

from .data import DataHandler
from ..utils.errata import ApiKeyError


class RunpodHandler(DataHandler):
    def __init__(self, api_key=None, data=None):
        self.api_key = api_key or os.getenv("RUNPOD_API_KEY")
        if not self.api_key:
            raise ApiKeyError()
        self.url = f"https://api.runpod.io/graphql?api_key={self.api_key}"
        self.data = data
        self.method = "POST"
        self.headers = {"content-type": "application/json"}

    def __call__(self):
        response = requests.request(
            method=self.method, url=self.url, headers=self.headers, json=self.data
        )

        if response.status_code != 200:
            print("Error:", response.text)

        return response
