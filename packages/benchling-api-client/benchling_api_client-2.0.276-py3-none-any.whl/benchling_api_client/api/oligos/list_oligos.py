from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.list_oligos_sort import ListOligosSort
from ...models.oligos_paginated_list import OligosPaginatedList
from ...types import Response, UNSET, Unset


def _get_kwargs(
    *,
    client: Client,
    sort: Union[Unset, ListOligosSort] = ListOligosSort.MODIFIEDAT,
    name: Union[Unset, str] = UNSET,
    bases: Union[Unset, str] = UNSET,
    folder_id: Union[Unset, str] = UNSET,
    mentioned_in: Union[Unset, str] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    registry_id: Union[Unset, None, str] = UNSET,
    schema_id: Union[Unset, str] = UNSET,
    mentions: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    entity_registry_idsany_of: Union[Unset, str] = UNSET,
    namesany_of: Union[Unset, str] = UNSET,
    namesany_ofcase_sensitive: Union[Unset, str] = UNSET,
    creator_ids: Union[Unset, str] = UNSET,
    returning: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/oligos".format(client.base_url)

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
    if not isinstance(name, Unset) and name is not None:
        params["name"] = name
    if not isinstance(bases, Unset) and bases is not None:
        params["bases"] = bases
    if not isinstance(folder_id, Unset) and folder_id is not None:
        params["folderId"] = folder_id
    if not isinstance(mentioned_in, Unset) and mentioned_in is not None:
        params["mentionedIn"] = mentioned_in
    if not isinstance(project_id, Unset) and project_id is not None:
        params["projectId"] = project_id
    if not isinstance(registry_id, Unset) and registry_id is not None:
        params["registryId"] = registry_id
    if not isinstance(schema_id, Unset) and schema_id is not None:
        params["schemaId"] = schema_id
    if not isinstance(mentions, Unset) and mentions is not None:
        params["mentions"] = mentions
    if not isinstance(ids, Unset) and ids is not None:
        params["ids"] = ids
    if not isinstance(entity_registry_idsany_of, Unset) and entity_registry_idsany_of is not None:
        params["entityRegistryIds.anyOf"] = entity_registry_idsany_of
    if not isinstance(namesany_of, Unset) and namesany_of is not None:
        params["names.anyOf"] = namesany_of
    if not isinstance(namesany_ofcase_sensitive, Unset) and namesany_ofcase_sensitive is not None:
        params["names.anyOf.caseSensitive"] = namesany_ofcase_sensitive
    if not isinstance(creator_ids, Unset) and creator_ids is not None:
        params["creatorIds"] = creator_ids
    if not isinstance(returning, Unset) and returning is not None:
        params["returning"] = returning

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[OligosPaginatedList, BadRequestError]]:
    if response.status_code == 200:
        response_200 = OligosPaginatedList.from_dict(response.json(), strict=False)

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json(), strict=False)

        return response_400
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[OligosPaginatedList, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    sort: Union[Unset, ListOligosSort] = ListOligosSort.MODIFIEDAT,
    name: Union[Unset, str] = UNSET,
    bases: Union[Unset, str] = UNSET,
    folder_id: Union[Unset, str] = UNSET,
    mentioned_in: Union[Unset, str] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    registry_id: Union[Unset, None, str] = UNSET,
    schema_id: Union[Unset, str] = UNSET,
    mentions: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    entity_registry_idsany_of: Union[Unset, str] = UNSET,
    namesany_of: Union[Unset, str] = UNSET,
    namesany_ofcase_sensitive: Union[Unset, str] = UNSET,
    creator_ids: Union[Unset, str] = UNSET,
    returning: Union[Unset, str] = UNSET,
) -> Response[Union[OligosPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        sort=sort,
        name=name,
        bases=bases,
        folder_id=folder_id,
        mentioned_in=mentioned_in,
        project_id=project_id,
        registry_id=registry_id,
        schema_id=schema_id,
        mentions=mentions,
        ids=ids,
        entity_registry_idsany_of=entity_registry_idsany_of,
        namesany_of=namesany_of,
        namesany_ofcase_sensitive=namesany_ofcase_sensitive,
        creator_ids=creator_ids,
        returning=returning,
    )

    response = client.httpx_client.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    sort: Union[Unset, ListOligosSort] = ListOligosSort.MODIFIEDAT,
    name: Union[Unset, str] = UNSET,
    bases: Union[Unset, str] = UNSET,
    folder_id: Union[Unset, str] = UNSET,
    mentioned_in: Union[Unset, str] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    registry_id: Union[Unset, None, str] = UNSET,
    schema_id: Union[Unset, str] = UNSET,
    mentions: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    entity_registry_idsany_of: Union[Unset, str] = UNSET,
    namesany_of: Union[Unset, str] = UNSET,
    namesany_ofcase_sensitive: Union[Unset, str] = UNSET,
    creator_ids: Union[Unset, str] = UNSET,
    returning: Union[Unset, str] = UNSET,
) -> Optional[Union[OligosPaginatedList, BadRequestError]]:
    """ List Oligos """

    return sync_detailed(
        client=client,
        sort=sort,
        name=name,
        bases=bases,
        folder_id=folder_id,
        mentioned_in=mentioned_in,
        project_id=project_id,
        registry_id=registry_id,
        schema_id=schema_id,
        mentions=mentions,
        ids=ids,
        entity_registry_idsany_of=entity_registry_idsany_of,
        namesany_of=namesany_of,
        namesany_ofcase_sensitive=namesany_ofcase_sensitive,
        creator_ids=creator_ids,
        returning=returning,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    sort: Union[Unset, ListOligosSort] = ListOligosSort.MODIFIEDAT,
    name: Union[Unset, str] = UNSET,
    bases: Union[Unset, str] = UNSET,
    folder_id: Union[Unset, str] = UNSET,
    mentioned_in: Union[Unset, str] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    registry_id: Union[Unset, None, str] = UNSET,
    schema_id: Union[Unset, str] = UNSET,
    mentions: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    entity_registry_idsany_of: Union[Unset, str] = UNSET,
    namesany_of: Union[Unset, str] = UNSET,
    namesany_ofcase_sensitive: Union[Unset, str] = UNSET,
    creator_ids: Union[Unset, str] = UNSET,
    returning: Union[Unset, str] = UNSET,
) -> Response[Union[OligosPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        sort=sort,
        name=name,
        bases=bases,
        folder_id=folder_id,
        mentioned_in=mentioned_in,
        project_id=project_id,
        registry_id=registry_id,
        schema_id=schema_id,
        mentions=mentions,
        ids=ids,
        entity_registry_idsany_of=entity_registry_idsany_of,
        namesany_of=namesany_of,
        namesany_ofcase_sensitive=namesany_ofcase_sensitive,
        creator_ids=creator_ids,
        returning=returning,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    sort: Union[Unset, ListOligosSort] = ListOligosSort.MODIFIEDAT,
    name: Union[Unset, str] = UNSET,
    bases: Union[Unset, str] = UNSET,
    folder_id: Union[Unset, str] = UNSET,
    mentioned_in: Union[Unset, str] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    registry_id: Union[Unset, None, str] = UNSET,
    schema_id: Union[Unset, str] = UNSET,
    mentions: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    entity_registry_idsany_of: Union[Unset, str] = UNSET,
    namesany_of: Union[Unset, str] = UNSET,
    namesany_ofcase_sensitive: Union[Unset, str] = UNSET,
    creator_ids: Union[Unset, str] = UNSET,
    returning: Union[Unset, str] = UNSET,
) -> Optional[Union[OligosPaginatedList, BadRequestError]]:
    """ List Oligos """

    return (
        await asyncio_detailed(
            client=client,
            sort=sort,
            name=name,
            bases=bases,
            folder_id=folder_id,
            mentioned_in=mentioned_in,
            project_id=project_id,
            registry_id=registry_id,
            schema_id=schema_id,
            mentions=mentions,
            ids=ids,
            entity_registry_idsany_of=entity_registry_idsany_of,
            namesany_of=namesany_of,
            namesany_ofcase_sensitive=namesany_ofcase_sensitive,
            creator_ids=creator_ids,
            returning=returning,
        )
    ).parsed
