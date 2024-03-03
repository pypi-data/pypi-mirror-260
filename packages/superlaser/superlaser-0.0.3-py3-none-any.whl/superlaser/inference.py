import os
from openai import OpenAI
from .utils.errata import ApiKeyError


class Client:
    def __init__(self, api_key, endpoint_id):
        self.api_key = api_key or os.getenv("RUNPOD_API_KEY")
        if not api_key:
            raise ApiKeyError()
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=f"https://api.runpod.ai/v2/{endpoint_id}/openai/v1",
        )
