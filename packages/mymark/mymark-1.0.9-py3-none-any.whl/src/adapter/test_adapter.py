from unittest.mock import patch

import pytest

from src.adapter.adapter_gpt import (  # Replace with the actual module and class names
    GPTModel,
    GPTRequest,
    GPTRole,
)


@pytest.mark.asyncio
async def test__get_single_response() -> None:
    mocked_response = {
        "id": "12345",
        "object": "chat.completion",
        "created": 1706622048,
        "model": "mocked_model",
        "choices": [
            {
                "index": 0,
                "message": {"role": "mocked_user", "content": "mocked_response"},
                "logprobs": None,
                "finish_reason": "stop",
            }
        ],
        "usage": {"prompt_tokens": 11, "completion_tokens": 7, "total_tokens": 18},
        "system_fingerprint": "fp_b57c83dd65",
    }

    with patch("src.adapter.adapter_gpt.GPTAdapter") as gpt_adapter:
        with patch("aiohttp.ClientSession") as mock_session:
            gpt_adapter._GPTAdapter__get_single_response.return_value = (  # pylint: disable=protected-access
                mocked_response
            )
            assert (
                mocked_response
                == gpt_adapter._GPTAdapter__get_single_response(  # pylint: disable=protected-access
                    mock_session,
                    GPTRequest("mocked_query", GPTRole.MOCKED_ROLE, GPTModel.MOCKED_MODEL),
                )
            )
