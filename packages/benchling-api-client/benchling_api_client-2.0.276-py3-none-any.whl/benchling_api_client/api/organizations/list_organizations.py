from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.list_organizations_sort import ListOrganizationsSort
from ...models.organizations_paginated_list import OrganizationsPaginatedList
from ...types import Response, UNSET, Unset


def _get_kwargs(
    *,
    client: Client,
    ids: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_includes: Union[Unset, str] = UNSET,
    namesany_of: Union[Unset, str] = UNSET,
    namesany_ofcase_sensitive: Union[Unset, str] = UNSET,
    has_members: Union[Unset, str] = UNSET,
    has_admins: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListOrganizationsSort] = ListOrganizationsSort.MODIFIEDAT,
) -> Dict[str, Any]:
    url = "{}/organizations".format(client.base_url)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    json_sort: Union[Unset, int] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value

    params: Dict[str, Any] = {}
    if not isinstance(ids, Unset) and ids is not None:
        params["ids"] = ids
    if not isinstance(name, Unset) and name is not None:
        params["name"] = name
    if not isinstance(name_includes, Unset) and name_includes is not None:
        params["nameIncludes"] = name_includes
    if not isinstance(namesany_of, Unset) and namesany_of is not None:
        params["names.anyOf"] = namesany_of
    if not isinstance(namesany_ofcase_sensitive, Unset) and namesany_ofcase_sensitive is not None:
        params["names.anyOf.caseSensitive"] = namesany_ofcase_sensitive
    if not isinstance(has_members, Unset) and has_members is not None:
        params["hasMembers"] = has_members
    if not isinstance(has_admins, Unset) and has_admins is not None:
        params["hasAdmins"] = has_admins
    if not isinstance(json_sort, Unset) and json_sort is not None:
        params["sort"] = json_sort

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[OrganizationsPaginatedList, BadRequestError]]:
    if response.status_code == 200:
        response_200 = OrganizationsPaginatedList.from_dict(response.json(), strict=False)

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json(), strict=False)

        return response_400
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[OrganizationsPaginatedList, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    ids: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_includes: Union[Unset, str] = UNSET,
    namesany_of: Union[Unset, str] = UNSET,
    namesany_ofcase_sensitive: Union[Unset, str] = UNSET,
    has_members: Union[Unset, str] = UNSET,
    has_admins: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListOrganizationsSort] = ListOrganizationsSort.MODIFIEDAT,
) -> Response[Union[OrganizationsPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        ids=ids,
        name=name,
        name_includes=name_includes,
        namesany_of=namesany_of,
        namesany_ofcase_sensitive=namesany_ofcase_sensitive,
        has_members=has_members,
        has_admins=has_admins,
        sort=sort,
    )

    response = client.httpx_client.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    ids: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_includes: Union[Unset, str] = UNSET,
    namesany_of: Union[Unset, str] = UNSET,
    namesany_ofcase_sensitive: Union[Unset, str] = UNSET,
    has_members: Union[Unset, str] = UNSET,
    has_admins: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListOrganizationsSort] = ListOrganizationsSort.MODIFIEDAT,
) -> Optional[Union[OrganizationsPaginatedList, BadRequestError]]:
    """Returns all organizations that the caller has permission to view. The following roles have view permission:
    - tenant admins
    - members of the organization
    """

    return sync_detailed(
        client=client,
        ids=ids,
        name=name,
        name_includes=name_includes,
        namesany_of=namesany_of,
        namesany_ofcase_sensitive=namesany_ofcase_sensitive,
        has_members=has_members,
        has_admins=has_admins,
        sort=sort,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    ids: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_includes: Union[Unset, str] = UNSET,
    namesany_of: Union[Unset, str] = UNSET,
    namesany_ofcase_sensitive: Union[Unset, str] = UNSET,
    has_members: Union[Unset, str] = UNSET,
    has_admins: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListOrganizationsSort] = ListOrganizationsSort.MODIFIEDAT,
) -> Response[Union[OrganizationsPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        ids=ids,
        name=name,
        name_includes=name_includes,
        namesany_of=namesany_of,
        namesany_ofcase_sensitive=namesany_ofcase_sensitive,
        has_members=has_members,
        has_admins=has_admins,
        sort=sort,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    ids: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_includes: Union[Unset, str] = UNSET,
    namesany_of: Union[Unset, str] = UNSET,
    namesany_ofcase_sensitive: Union[Unset, str] = UNSET,
    has_members: Union[Unset, str] = UNSET,
    has_admins: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListOrganizationsSort] = ListOrganizationsSort.MODIFIEDAT,
) -> Optional[Union[OrganizationsPaginatedList, BadRequestError]]:
    """Returns all organizations that the caller has permission to view. The following roles have view permission:
    - tenant admins
    - members of the organization
    """

    return (
        await asyncio_detailed(
            client=client,
            ids=ids,
            name=name,
            name_includes=name_includes,
            namesany_of=namesany_of,
            namesany_ofcase_sensitive=namesany_ofcase_sensitive,
            has_members=has_members,
            has_admins=has_admins,
            sort=sort,
        )
    ).parsed
