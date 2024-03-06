import os
import warnings
from enum import Enum
from typing import Any

import requests
from adapter.adapter import Adapter, Request
from urllib3.exceptions import InsecureRequestWarning

# Suppress InsecureRequestWarning
warnings.filterwarnings("ignore", category=InsecureRequestWarning)


class GPTModel(str, Enum):
    GPT3_5TURBO = "GPT3_5TURBO"
    GPT3_5TURBOLATEST = "GPT3_5TURBOLATEST"
    # Not suitable for high traffic
    GPT3_5TURBO_UNLIMITED = "GPT3_5TURBO_UNLIMITED"
    GPT4 = "GPT4"  # Never ever use this
    GPT4LATEST = "GPT4LATEST"


class GPTRole(str, Enum):
    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"


class GPTRequest(Request):  # pylint: disable=too-few-public-methods
    def __init__(
        self,
        query: list[dict[str, Any]],
        model: GPTModel = GPTModel.GPT3_5TURBOLATEST,
        temperature: float = 0.7,
    ) -> None:
        """Initialises with a query, the GPTRole and the GPTModel"""
        super().__init__()
        self._query = query
        self.model = model
        self.temperature = temperature

    @property
    def serialised(self) -> dict[str, Any]:
        return {
            "query": self.query,
            "model": self.model.value,
            "temperature": self.temperature,
        }

    @property
    def query(self) -> list[dict[str, Any]]:
        return self._query


class ServerAdapter(Adapter):
    def __init__(self) -> None:
        self.host_address = f"https://{os.getenv('SERVER_HOST')}:8081"

    def get_mark_scheme(self, module_name: str, exercise_name: str) -> str:
        response = requests.get(
            f"{self.host_address}/modules/{module_name}/exercises/{exercise_name}/mark_scheme",
            headers={"Authorization": os.getenv("SERVER_API_KEY")},
            verify=False,
            timeout=10,
        )
        response.raise_for_status()
        return str(response.json()["mark_scheme"])

    def get_response(self, request: GPTRequest) -> str:
        try:
            response = requests.post(
                f"{self.host_address}/gpt",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": os.getenv("SERVER_API_KEY"),
                },
                json=request.serialised,
                verify=False,
                timeout=10,
            )
            response.raise_for_status()
        except Exception as _:
            response = requests.post(
                f"{self.host_address}/gpt",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": os.getenv("SERVER_API_KEY"),
                },
                json=request.serialised,
                verify=False,
                timeout=10,
            )
            response.raise_for_status()
        return str(response.json()["response"])
