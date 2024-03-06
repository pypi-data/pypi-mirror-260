from __future__ import annotations

from openai import OpenAI as BaseOpenAI
from openai.resources.chat.chat import Chat as BaseChat
from openai.resources.chat.completions import Completions as BaseCompletions
from openai.resources.embeddings import Embeddings as BaseEmbeddings

from typing import TYPE_CHECKING, Dict, List, Union, Optional, overload
from typing_extensions import Literal

import httpx

from openai._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from openai._utils import required_args, maybe_transform
from openai._resource import SyncAPIResource, AsyncAPIResource
from openai._response import to_raw_response_wrapper, async_to_raw_response_wrapper
from openai._streaming import Stream, AsyncStream
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionChunk,
    ChatCompletionToolParam,
    ChatCompletionMessageParam,
    ChatCompletionToolChoiceOptionParam,
    completion_create_params,
)
from openai._base_client import make_request_options

from .functions import chat_completion

import base64
from typing import TYPE_CHECKING, List, Union, Iterable, cast
from typing_extensions import Literal

import httpx

from openai.types import CreateEmbeddingResponse, embedding_create_params
from openai._utils import is_given, maybe_transform
from openai._extras import numpy as np
from openai._extras import has_numpy


class OpenAI(BaseOpenAI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chat = Chat(self)
        
class Chat(BaseChat):
    def __init__(self, client: OpenAI):
        super().__init__(client)
        self.completions = Completions(client)

class Completions(BaseCompletions):
    @required_args(["messages", "model"], ["messages", "model", "stream"])
    def create(
        self,
        *,
        messages: List[ChatCompletionMessageParam],
        model: Union[
            str,
            Literal[
                "gpt-4-0125-preview",
                "gpt-4-turbo-preview",
                "gpt-4-1106-preview",
                "gpt-4-vision-preview",
                "gpt-4",
                "gpt-4-0314",
                "gpt-4-0613",
                "gpt-4-32k",
                "gpt-4-32k-0314",
                "gpt-4-32k-0613",
                "gpt-3.5-turbo",
                "gpt-3.5-turbo-16k",
                "gpt-3.5-turbo-0301",
                "gpt-3.5-turbo-0613",
                "gpt-3.5-turbo-1106",
                "gpt-3.5-turbo-16k-0613",
            ],
        ],
        frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        function_call: completion_create_params.FunctionCall | NotGiven = NOT_GIVEN,
        functions: List[completion_create_params.Function] | NotGiven = NOT_GIVEN,
        logit_bias: Optional[Dict[str, int]] | NotGiven = NOT_GIVEN,
        max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        n: Optional[int] | NotGiven = NOT_GIVEN,
        presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        response_format: completion_create_params.ResponseFormat | NotGiven = NOT_GIVEN,
        seed: Optional[int] | NotGiven = NOT_GIVEN,
        stop: Union[Optional[str], List[str]] | NotGiven = NOT_GIVEN,
        stream: Optional[Literal[False]] | Literal[True] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        tool_choice: ChatCompletionToolChoiceOptionParam | NotGiven = NOT_GIVEN,
        tools: List[ChatCompletionToolParam] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        user: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChatCompletion | Stream[ChatCompletionChunk]:
        model_params = {
            "messages": messages,
            "model": model,
            "stream": stream,
            "frequency_penalty": frequency_penalty,
            "function_call": function_call,
            "functions": functions,
            "logit_bias": logit_bias,
            "max_tokens": max_tokens,
            "n": n,
            "presence_penalty": presence_penalty,
            "response_format": response_format,
            "seed": seed,
            "stop": stop,
            "stream": stream,
            "temperature": temperature,
            "tool_choice": tool_choice,
            "tools": tools,
            "top_p": top_p,
            "user": user,
        }
        model_params = {k: v for k, v in model_params.items() if v != NOT_GIVEN}
        response = chat_completion(model_params)
        
        if response.status_code == 200:
            response = response.json()
            response = ChatCompletion(**response)
            return response
        else:
            error_message = response.text
            return f"Request failed with status code {response.status_code}: {error_message}"


# class Embeddings(BaseEmbeddings):
#     def create(
#         self,
#         *,
#         input: Union[str, List[str], Iterable[int], Iterable[Iterable[int]]],
#         model: Union[str, Literal["text-embedding-ada-002", "text-embedding-3-small", "text-embedding-3-large"]],
#         dimensions: int | NotGiven = NOT_GIVEN,
#         encoding_format: Literal["float", "base64"] | NotGiven = NOT_GIVEN,
#         user: str | NotGiven = NOT_GIVEN,
#         # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
#         # The extra values given here take precedence over values defined on the client or passed to this method.
#         extra_headers: Headers | None = None,
#         extra_query: Query | None = None,
#         extra_body: Body | None = None,
#         timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
#     ) -> CreateEmbeddingResponse:
#         params = {
#             "input": input,
#             "model": model,
#             "user": user,
#             "dimensions": dimensions,
#             "encoding_format": encoding_format,
#         }
#         if not is_given(encoding_format) and has_numpy():
#             params["encoding_format"] = "base64"

#         def parser(obj: CreateEmbeddingResponse) -> CreateEmbeddingResponse:
#             if is_given(encoding_format):
#                 # don't modify the response object if a user explicitly asked for a format
#                 return obj

#             for embedding in obj.data:
#                 data = cast(object, embedding.embedding)
#                 if not isinstance(data, str):
#                     # numpy is not installed / base64 optimisation isn't enabled for this model yet
#                     continue

#                 embedding.embedding = np.frombuffer(  # type: ignore[no-untyped-call]
#                     base64.b64decode(data), dtype="float32"
#                 ).tolist()

#             return obj

#         return self._post(
#             "/embeddings",
#             body=maybe_transform(params, embedding_create_params.EmbeddingCreateParams),
#             options=make_request_options(
#                 extra_headers=extra_headers,
#                 extra_query=extra_query,
#                 extra_body=extra_body,
#                 timeout=timeout,
#                 post_parser=parser,
#             ),
#             cast_to=CreateEmbeddingResponse,
#         )