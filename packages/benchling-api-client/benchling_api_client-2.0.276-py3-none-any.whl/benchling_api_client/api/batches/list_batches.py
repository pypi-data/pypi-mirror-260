from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.batches_paginated_list import BatchesPaginatedList
from ...models.list_batches_sort import ListBatchesSort
from ...types import Response, UNSET, Unset


def _get_kwargs(
    *,
    client: Client,
    sort: Union[Unset, ListBatchesSort] = ListBatchesSort.MODIFIEDAT,
    schema_id: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    creator_ids: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/batches".format(client.base_url)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    json_sort: Union[Unset, int] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value

    params: Dict[str, Any] = {}
    if not isinstance(json_sort, Unset) and json_sort is not None:
        params["sort"] = json_sort
    if not isinstance(schema_id, Unset) and schema_id is not None:
        params["schemaId"] = schema_id
    if not isinstance(ids, Unset) and ids is not None:
        params["ids"] = ids
    if not isinstance(creator_ids, Unset) and creator_ids is not None:
        params["creatorIds"] = creator_ids

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[BatchesPaginatedList, BadRequestError]]:
    if response.status_code == 200:
        response_200 = BatchesPaginatedList.from_dict(response.json(), strict=False)

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json(), strict=False)

        return response_400
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[BatchesPaginatedList, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    sort: Union[Unset, ListBatchesSort] = ListBatchesSort.MODIFIEDAT,
    schema_id: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    creator_ids: Union[Unset, str] = UNSET,
) -> Response[Union[BatchesPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        sort=sort,
        schema_id=schema_id,
        ids=ids,
        creator_ids=creator_ids,
    )

    response = client.httpx_client.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    sort: Union[Unset, ListBatchesSort] = ListBatchesSort.MODIFIEDAT,
    schema_id: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    creator_ids: Union[Unset, str] = UNSET,
) -> Optional[Union[BatchesPaginatedList, BadRequestError]]:
    """ List batches """

    return sync_detailed(
        client=client,
        sort=sort,
        schema_id=schema_id,
        ids=ids,
        creator_ids=creator_ids,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    sort: Union[Unset, ListBatchesSort] = ListBatchesSort.MODIFIEDAT,
    schema_id: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    creator_ids: Union[Unset, str] = UNSET,
) -> Response[Union[BatchesPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        sort=sort,
        schema_id=schema_id,
        ids=ids,
        creator_ids=creator_ids,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    sort: Union[Unset, ListBatchesSort] = ListBatchesSort.MODIFIEDAT,
    schema_id: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    creator_ids: Union[Unset, str] = UNSET,
) -> Optional[Union[BatchesPaginatedList, BadRequestError]]:
    """ List batches """

    return (
        await asyncio_detailed(
            client=client,
            sort=sort,
            schema_id=schema_id,
            ids=ids,
            creator_ids=creator_ids,
        )
    ).parsed
