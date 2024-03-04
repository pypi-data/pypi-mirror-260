#https://github.com/openai/openai-python/issues/715#issuecomment-1809203346

import datetime
from unittest.mock import patch

from openai.types.chat import ChatCompletionMessage
from openai.types.chat.chat_completion import ChatCompletion, Choice
from openai.types.completion_usage import CompletionUsage
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk, ChoiceDelta
from openai.types.chat.chat_completion_chunk import Choice as StreamChoice


def mock_chat_completion(response: str, model: str = "gpt-3.5-turbo") -> ChatCompletion:
    return ChatCompletion(
        id="foo",
        model=model,
        object="chat.completion",
        choices=[
            Choice(
                finish_reason="stop",
                index=0,
                message=ChatCompletionMessage(
                    content=response,
                    role="assistant",
                ),
            )
        ],
        usage=CompletionUsage(
            prompt_tokens=0,
            completion_tokens=10,
            total_tokens=10,
        ),
        created=int(datetime.datetime.now().timestamp()),
    )


def mock_stream_chat_completion(response: str, model: str = "gpt-3.5-turbo"):
    for token in response:
        yield ChatCompletionChunk(
            id="foo",
            model=model,
            object="chat.completion.chunk",
            choices=[
                StreamChoice(
                    index=0,
                    finish_reason=None,
                    delta=ChoiceDelta(
                        content=token,
                        role="assistant",
                    )
                ),
            ],
            created=int(datetime.datetime.now().timestamp()),
        )


@patch("openai.resources.chat.Completions.create")
def test_chat_completion(openai_create):
    from openai import OpenAI
    EXPECTED_RESPONSE = "The mock is working! ;)"
    openai_create.return_value = mock_chat_completion(EXPECTED_RESPONSE)
    client = OpenAI(api_key="sk-...")
    r = client.chat.completions.create(
        messages=[{"role": "user", "content": "Do you know any jokes?"}],
        model="gpt-3.5-turbo",
    )
    response = r.choices[0].message.content
    assert response == EXPECTED_RESPONSE


@patch("openai.resources.chat.Completions.create")
def test_stream_chat_completion(openai_create):
    print("aaa  ")
    from openai import OpenAI
    EXPECTED_RESPONSE = "The mock is STILL working! ;)"
    openai_create.return_value = mock_stream_chat_completion(EXPECTED_RESPONSE)
    client = OpenAI(api_key="sk-...")
    stream = client.chat.completions.create(
        messages=[{"role": "user", "content": "Do you know any jokes?"}],
        model="gpt-3.5-turbo",
        stream=True,
    )

    response = ""
    chunk_count = 0
    for chunk in stream:
        response += (chunk.choices[0].delta.content or "")
        print("Chunk:",chunk)
        chunk_count += 1
    assert response == EXPECTED_RESPONSE
    assert chunk_count == len(EXPECTED_RESPONSE)
    
test_stream_chat_completion()