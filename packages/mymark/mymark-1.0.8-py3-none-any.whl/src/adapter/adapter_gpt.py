import asyncio
from enum import Enum
from typing import Any

from aiohttp import ClientSession

from src.adapter.adapter import Adapter, Request

DEFAULT_API_KEY_GPT_3 = "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"
DEFAULT_API_KEY_GPT_4 = "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"


class GPTModel(Enum):
    """
    Enum for models of GPT API.
    """

    GPT3_5TURBO = "gpt-3.5-turbo"
    GPT3_5TURBOLATEST = "gpt-3.5-turbo-0125"
    # Not suitable for high traffic
    GPT3_5TURBO_UNLIMITED = "gpt-3.5-turbo"
    GPT4 = "gpt-4" # Never ever use this
    GPT4LATEST = "gpt-4-turbo-preview"

    # for testing
    MOCKED_MODEL = "mocked_model"


class GPTRole(Enum):
    """
    Enum for roles in GTP API requests.
    """

    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"

    # for testing
    MOCKED_ROLE = "mocked_role"


GPT_KEY_MAP = {
    GPTModel.GPT3_5TURBO: DEFAULT_API_KEY_GPT_3,
    GPTModel.GPT3_5TURBOLATEST: DEFAULT_API_KEY_GPT_3,
    GPTModel.GPT3_5TURBO_UNLIMITED: DEFAULT_API_KEY_GPT_4,
    GPTModel.GPT4: DEFAULT_API_KEY_GPT_4,
    GPTModel.GPT4LATEST: DEFAULT_API_KEY_GPT_4,
    # for testing
    GPTModel.MOCKED_MODEL: "mocked_key",
}


class GPTRequest(Request):  # pylint: disable=too-few-public-methods
    def __init__(
        self,
        query: str,
        role: GPTRole = GPTRole.USER,
        model: GPTModel = GPTModel.GPT3_5TURBOLATEST,
        temperature: float = 0.7,
    ) -> None:
        """Initialises with a query, the GPTRole and the GPTModel"""
        super().__init__()
        self._query = query
        self.role = role
        self.model = model
        self.temperature = temperature

    @property
    def query(self) -> str:
        return self._query


class GPTAdapter(Adapter):
    def get_response(self, request: GPTRequest) -> str:
        """Processes a GPTRequest and returns the response"""
        result: list[str] = asyncio.run(self.__get_responses_async([request]))
        return result[0]

    async def __get_single_response(self, session: ClientSession, request: GPTRequest) -> Any:
        """Returns an async task for request that holds the GPT response"""
        # Post the request
        async with session.post(
            "https://api.openai.com/v1/chat/completions",
            json={
                "model": request.model.value,
                "messages": [{"role": request.role.value, "content": request.query}],
                "temperature": request.temperature,
            },
            headers={
                "Authorization": f"Bearer {GPT_KEY_MAP[GPTModel(request.model)]}",
                "Content-Type": "application/json",
            },
        ) as response:
            # Get the result as json
            result = await response.json()
            return result

    def get_responses(self, requests: list[GPTRequest]) -> list[str]:
        """Processes many GPTRequests and the response"""
        return asyncio.run(self.__get_responses_async(requests))

    async def __get_responses_async(self, requests: list[GPTRequest]) -> Any:
        async with ClientSession() as session:
            # Map each request to an async task
            tasks = [self.__get_single_response(session, request) for request in requests]

            results: list[dict[str, Any]] = await asyncio.gather(*tasks)

            try:
                # Extract content from each json response dict
                return [completion["choices"][0]["message"]["content"] for completion in results]
            except Exception as e:
                print("Error! Something went wrong with OpenAI call. Response:\n")
                print(results)
                raise e
