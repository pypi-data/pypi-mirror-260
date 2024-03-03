import os
from openai import OpenAI

from .utils.errata import ApiKeyError


class SuperLaser:
    def __init__(self, endpoint_id, model_name, api_key=None, stream=False, chat=True):
        self.api_key = api_key or os.getenv("RUNPOD_API_KEY")
        if not api_key:
            raise ApiKeyError()
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=f"https://api.runpod.ai/v2/{endpoint_id}/openai/v1",
        )
        self.model_name = model_name
        self.stream = stream
        self.chat = chat

    def __call__(self, prompt):
        if self.chat:
            self._chat_completion(prompt)
        else:
            self._non_chat_completion(prompt)

    def _chat_completion(self, user_message):
        if self.stream:
            response_stream = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": user_message}],
                temperature=0,
                max_tokens=100,
                stream=True,
            )

            for response in response_stream:
                print(response.choices[0].delta.content or "", end="", flush=True)
        else:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": user_message}],
                temperature=0,
                max_tokens=100,
            )

            print(response.choices[0].message.content)

    def _non_chat_completion(self, prompt):
        if self.stream:
            response_stream = self.client.completions.create(
                model=self.model_name,
                prompt=prompt,
                temperature=0,
                max_tokens=100,
                stream=True,
            )

            for response in response_stream:
                print(response.choices[0].text or "", end="", flush=True)
        else:
            response = self.client.completions.create(
                model=self.model_name,
                prompt=prompt,
                temperature=0,
                max_tokens=100,
            )

            print(response.choices[0].text)
