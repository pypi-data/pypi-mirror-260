# This file was auto-generated by Fern from our API Definition.

import typing
import urllib.parse
from json.decoder import JSONDecodeError

from ..core.api_error import ApiError
from ..core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ..core.jsonable_encoder import jsonable_encoder
from ..core.remove_none_from_dict import remove_none_from_dict
from ..core.request_options import RequestOptions
from ..errors.unprocessable_entity_error import UnprocessableEntityError
from ..types.http_validation_error import HttpValidationError
from ..types.message_out import MessageOut
from ..types.message_out_dto import MessageOutDto
from ..types.model import Model
from ..types.tools import Tools

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class MessageClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def submit(
        self,
        *,
        content: str,
        model: typing.Optional[Model] = OMIT,
        tools: typing.Optional[typing.Sequence[Tools]] = OMIT,
        conversation_id: typing.Optional[str] = OMIT,
        conversation_name: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> MessageOut:
        """
        Parameters:
            - content: str.

            - model: typing.Optional[Model].

            - tools: typing.Optional[typing.Sequence[Tools]].

            - conversation_id: typing.Optional[str].

            - conversation_name: typing.Optional[str].

            - request_options: typing.Optional[RequestOptions]. Request-specific configuration.
        ---
        from athena import Model, Tools
        from athena.client import Athena

        client = Athena(
            api_key="YOUR_API_KEY",
            token="YOUR_TOKEN",
        )
        client.message.submit(
            content="visit www.athenaintelligence.ai and summarize the website in one paragraph",
            model=Model.GPT_4_TURBO_PREVIEW,
            tools=[Tools.SEARCH, Tools.BROWSE, Tools.SEARCH],
        )
        """
        _request: typing.Dict[str, typing.Any] = {"content": content}
        if model is not OMIT:
            _request["model"] = model.value if model is not None else None
        if tools is not OMIT:
            _request["tools"] = tools
        if conversation_id is not OMIT:
            _request["conversation_id"] = conversation_id
        if conversation_name is not OMIT:
            _request["conversation_name"] = conversation_name
        _response = self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", "api/v0/message"),
            params=jsonable_encoder(
                request_options.get("additional_query_parameters") if request_options is not None else None
            ),
            json=jsonable_encoder(_request)
            if request_options is None or request_options.get("additional_body_parameters") is None
            else {
                **jsonable_encoder(_request),
                **(jsonable_encoder(remove_none_from_dict(request_options.get("additional_body_parameters", {})))),
            },
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self._client_wrapper.get_headers(),
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            timeout=request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else 60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(MessageOut, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def get(self, id: str, *, request_options: typing.Optional[RequestOptions] = None) -> MessageOutDto:
        """
        Parameters:
            - id: str.

            - request_options: typing.Optional[RequestOptions]. Request-specific configuration.
        ---
        from athena.client import Athena

        client = Athena(
            api_key="YOUR_API_KEY",
            token="YOUR_TOKEN",
        )
        client.message.get(
            id="id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", f"api/v0/message/{jsonable_encoder(id)}"),
            params=jsonable_encoder(
                request_options.get("additional_query_parameters") if request_options is not None else None
            ),
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self._client_wrapper.get_headers(),
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            timeout=request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else 60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(MessageOutDto, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncMessageClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def submit(
        self,
        *,
        content: str,
        model: typing.Optional[Model] = OMIT,
        tools: typing.Optional[typing.Sequence[Tools]] = OMIT,
        conversation_id: typing.Optional[str] = OMIT,
        conversation_name: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> MessageOut:
        """
        Parameters:
            - content: str.

            - model: typing.Optional[Model].

            - tools: typing.Optional[typing.Sequence[Tools]].

            - conversation_id: typing.Optional[str].

            - conversation_name: typing.Optional[str].

            - request_options: typing.Optional[RequestOptions]. Request-specific configuration.
        ---
        from athena import Model, Tools
        from athena.client import AsyncAthena

        client = AsyncAthena(
            api_key="YOUR_API_KEY",
            token="YOUR_TOKEN",
        )
        await client.message.submit(
            content="visit www.athenaintelligence.ai and summarize the website in one paragraph",
            model=Model.GPT_4_TURBO_PREVIEW,
            tools=[Tools.SEARCH, Tools.BROWSE, Tools.SEARCH],
        )
        """
        _request: typing.Dict[str, typing.Any] = {"content": content}
        if model is not OMIT:
            _request["model"] = model.value if model is not None else None
        if tools is not OMIT:
            _request["tools"] = tools
        if conversation_id is not OMIT:
            _request["conversation_id"] = conversation_id
        if conversation_name is not OMIT:
            _request["conversation_name"] = conversation_name
        _response = await self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", "api/v0/message"),
            params=jsonable_encoder(
                request_options.get("additional_query_parameters") if request_options is not None else None
            ),
            json=jsonable_encoder(_request)
            if request_options is None or request_options.get("additional_body_parameters") is None
            else {
                **jsonable_encoder(_request),
                **(jsonable_encoder(remove_none_from_dict(request_options.get("additional_body_parameters", {})))),
            },
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self._client_wrapper.get_headers(),
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            timeout=request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else 60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(MessageOut, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def get(self, id: str, *, request_options: typing.Optional[RequestOptions] = None) -> MessageOutDto:
        """
        Parameters:
            - id: str.

            - request_options: typing.Optional[RequestOptions]. Request-specific configuration.
        ---
        from athena.client import AsyncAthena

        client = AsyncAthena(
            api_key="YOUR_API_KEY",
            token="YOUR_TOKEN",
        )
        await client.message.get(
            id="id",
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", f"api/v0/message/{jsonable_encoder(id)}"),
            params=jsonable_encoder(
                request_options.get("additional_query_parameters") if request_options is not None else None
            ),
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self._client_wrapper.get_headers(),
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            timeout=request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else 60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(MessageOutDto, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
