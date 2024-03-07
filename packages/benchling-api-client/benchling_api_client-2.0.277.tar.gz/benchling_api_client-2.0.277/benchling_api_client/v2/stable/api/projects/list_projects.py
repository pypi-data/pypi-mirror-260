from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.list_projects_sort import ListProjectsSort
from ...models.projects_paginated_list import ProjectsPaginatedList
from ...types import Response, UNSET, Unset


def _get_kwargs(
    *,
    client: Client,
    sort: Union[Unset, ListProjectsSort] = ListProjectsSort.MODIFIEDAT,
    ids: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/projects".format(client.base_url)

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
    if not isinstance(ids, Unset) and ids is not None:
        params["ids"] = ids
    if not isinstance(name, Unset) and name is not None:
        params["name"] = name

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[ProjectsPaginatedList]:
    if response.status_code == 200:
        response_200 = ProjectsPaginatedList.from_dict(response.json(), strict=False)

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[ProjectsPaginatedList]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    sort: Union[Unset, ListProjectsSort] = ListProjectsSort.MODIFIEDAT,
    ids: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
) -> Response[ProjectsPaginatedList]:
    kwargs = _get_kwargs(
        client=client,
        sort=sort,
        ids=ids,
        name=name,
    )

    response = client.httpx_client.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    sort: Union[Unset, ListProjectsSort] = ListProjectsSort.MODIFIEDAT,
    ids: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
) -> Optional[ProjectsPaginatedList]:
    """ List projects """

    return sync_detailed(
        client=client,
        sort=sort,
        ids=ids,
        name=name,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    sort: Union[Unset, ListProjectsSort] = ListProjectsSort.MODIFIEDAT,
    ids: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
) -> Response[ProjectsPaginatedList]:
    kwargs = _get_kwargs(
        client=client,
        sort=sort,
        ids=ids,
        name=name,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    sort: Union[Unset, ListProjectsSort] = ListProjectsSort.MODIFIEDAT,
    ids: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
) -> Optional[ProjectsPaginatedList]:
    """ List projects """

    return (
        await asyncio_detailed(
            client=client,
            sort=sort,
            ids=ids,
            name=name,
        )
    ).parsed
