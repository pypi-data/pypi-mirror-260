from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.request_fulfillments_paginated_list import RequestFulfillmentsPaginatedList
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    entry_id: str,
) -> Dict[str, Any]:
    url = "{}/request-fulfillments".format(client.base_url)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    params: Dict[str, Any] = {
        "entryId": entry_id,
    }

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[RequestFulfillmentsPaginatedList, BadRequestError]]:
    if response.status_code == 200:
        response_200 = RequestFulfillmentsPaginatedList.from_dict(response.json(), strict=False)

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json(), strict=False)

        return response_400
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[RequestFulfillmentsPaginatedList, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    entry_id: str,
) -> Response[Union[RequestFulfillmentsPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        entry_id=entry_id,
    )

    response = client.httpx_client.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    entry_id: str,
) -> Optional[Union[RequestFulfillmentsPaginatedList, BadRequestError]]:
    """ List Request Fulfillments """

    return sync_detailed(
        client=client,
        entry_id=entry_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    entry_id: str,
) -> Response[Union[RequestFulfillmentsPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        entry_id=entry_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    entry_id: str,
) -> Optional[Union[RequestFulfillmentsPaginatedList, BadRequestError]]:
    """ List Request Fulfillments """

    return (
        await asyncio_detailed(
            client=client,
            entry_id=entry_id,
        )
    ).parsed
