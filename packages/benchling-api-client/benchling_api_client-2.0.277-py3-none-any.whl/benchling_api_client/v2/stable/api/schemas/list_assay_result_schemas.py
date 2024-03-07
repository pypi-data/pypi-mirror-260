from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.assay_result_schemas_paginated_list import AssayResultSchemasPaginatedList
from ...models.bad_request_error import BadRequestError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/assay-result-schemas".format(client.base_url)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[AssayResultSchemasPaginatedList, BadRequestError]]:
    if response.status_code == 200:
        response_200 = AssayResultSchemasPaginatedList.from_dict(response.json(), strict=False)

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json(), strict=False)

        return response_400
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[AssayResultSchemasPaginatedList, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
) -> Response[Union[AssayResultSchemasPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
    )

    response = client.httpx_client.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
) -> Optional[Union[AssayResultSchemasPaginatedList, BadRequestError]]:
    """ List assay result schemas """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
) -> Response[Union[AssayResultSchemasPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
) -> Optional[Union[AssayResultSchemasPaginatedList, BadRequestError]]:
    """ List assay result schemas """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
