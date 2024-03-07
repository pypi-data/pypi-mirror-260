from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.entries_paginated_list import EntriesPaginatedList
from ...models.list_entries_review_status import ListEntriesReviewStatus
from ...models.list_entries_sort import ListEntriesSort
from ...types import Response, UNSET, Unset


def _get_kwargs(
    *,
    client: Client,
    sort: Union[Unset, ListEntriesSort] = ListEntriesSort.MODIFIEDAT,
    name: Union[Unset, str] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    review_status: Union[Unset, ListEntriesReviewStatus] = UNSET,
    mentioned_in: Union[Unset, str] = UNSET,
    mentions: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    schema_id: Union[Unset, str] = UNSET,
    namesany_of: Union[Unset, str] = UNSET,
    namesany_ofcase_sensitive: Union[Unset, str] = UNSET,
    assigned_reviewer_idsany_of: Union[Unset, str] = UNSET,
    creator_ids: Union[Unset, str] = UNSET,
    author_idsany_of: Union[Unset, str] = UNSET,
    display_ids: Union[Unset, str] = UNSET,
    returning: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/entries".format(client.base_url)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    json_sort: Union[Unset, int] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value

    json_review_status: Union[Unset, int] = UNSET
    if not isinstance(review_status, Unset):
        json_review_status = review_status.value

    params: Dict[str, Any] = {}
    if not isinstance(json_sort, Unset) and json_sort is not None:
        params["sort"] = json_sort
    if not isinstance(name, Unset) and name is not None:
        params["name"] = name
    if not isinstance(project_id, Unset) and project_id is not None:
        params["projectId"] = project_id
    if not isinstance(json_review_status, Unset) and json_review_status is not None:
        params["reviewStatus"] = json_review_status
    if not isinstance(mentioned_in, Unset) and mentioned_in is not None:
        params["mentionedIn"] = mentioned_in
    if not isinstance(mentions, Unset) and mentions is not None:
        params["mentions"] = mentions
    if not isinstance(ids, Unset) and ids is not None:
        params["ids"] = ids
    if not isinstance(schema_id, Unset) and schema_id is not None:
        params["schemaId"] = schema_id
    if not isinstance(namesany_of, Unset) and namesany_of is not None:
        params["names.anyOf"] = namesany_of
    if not isinstance(namesany_ofcase_sensitive, Unset) and namesany_ofcase_sensitive is not None:
        params["names.anyOf.caseSensitive"] = namesany_ofcase_sensitive
    if not isinstance(assigned_reviewer_idsany_of, Unset) and assigned_reviewer_idsany_of is not None:
        params["assignedReviewerIds.anyOf"] = assigned_reviewer_idsany_of
    if not isinstance(creator_ids, Unset) and creator_ids is not None:
        params["creatorIds"] = creator_ids
    if not isinstance(author_idsany_of, Unset) and author_idsany_of is not None:
        params["authorIds.anyOf"] = author_idsany_of
    if not isinstance(display_ids, Unset) and display_ids is not None:
        params["displayIds"] = display_ids
    if not isinstance(returning, Unset) and returning is not None:
        params["returning"] = returning

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[EntriesPaginatedList, BadRequestError]]:
    if response.status_code == 200:
        response_200 = EntriesPaginatedList.from_dict(response.json(), strict=False)

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json(), strict=False)

        return response_400
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[EntriesPaginatedList, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    sort: Union[Unset, ListEntriesSort] = ListEntriesSort.MODIFIEDAT,
    name: Union[Unset, str] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    review_status: Union[Unset, ListEntriesReviewStatus] = UNSET,
    mentioned_in: Union[Unset, str] = UNSET,
    mentions: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    schema_id: Union[Unset, str] = UNSET,
    namesany_of: Union[Unset, str] = UNSET,
    namesany_ofcase_sensitive: Union[Unset, str] = UNSET,
    assigned_reviewer_idsany_of: Union[Unset, str] = UNSET,
    creator_ids: Union[Unset, str] = UNSET,
    author_idsany_of: Union[Unset, str] = UNSET,
    display_ids: Union[Unset, str] = UNSET,
    returning: Union[Unset, str] = UNSET,
) -> Response[Union[EntriesPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        sort=sort,
        name=name,
        project_id=project_id,
        review_status=review_status,
        mentioned_in=mentioned_in,
        mentions=mentions,
        ids=ids,
        schema_id=schema_id,
        namesany_of=namesany_of,
        namesany_ofcase_sensitive=namesany_ofcase_sensitive,
        assigned_reviewer_idsany_of=assigned_reviewer_idsany_of,
        creator_ids=creator_ids,
        author_idsany_of=author_idsany_of,
        display_ids=display_ids,
        returning=returning,
    )

    response = client.httpx_client.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    sort: Union[Unset, ListEntriesSort] = ListEntriesSort.MODIFIEDAT,
    name: Union[Unset, str] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    review_status: Union[Unset, ListEntriesReviewStatus] = UNSET,
    mentioned_in: Union[Unset, str] = UNSET,
    mentions: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    schema_id: Union[Unset, str] = UNSET,
    namesany_of: Union[Unset, str] = UNSET,
    namesany_ofcase_sensitive: Union[Unset, str] = UNSET,
    assigned_reviewer_idsany_of: Union[Unset, str] = UNSET,
    creator_ids: Union[Unset, str] = UNSET,
    author_idsany_of: Union[Unset, str] = UNSET,
    display_ids: Union[Unset, str] = UNSET,
    returning: Union[Unset, str] = UNSET,
) -> Optional[Union[EntriesPaginatedList, BadRequestError]]:
    """ List notebook entries """

    return sync_detailed(
        client=client,
        sort=sort,
        name=name,
        project_id=project_id,
        review_status=review_status,
        mentioned_in=mentioned_in,
        mentions=mentions,
        ids=ids,
        schema_id=schema_id,
        namesany_of=namesany_of,
        namesany_ofcase_sensitive=namesany_ofcase_sensitive,
        assigned_reviewer_idsany_of=assigned_reviewer_idsany_of,
        creator_ids=creator_ids,
        author_idsany_of=author_idsany_of,
        display_ids=display_ids,
        returning=returning,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    sort: Union[Unset, ListEntriesSort] = ListEntriesSort.MODIFIEDAT,
    name: Union[Unset, str] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    review_status: Union[Unset, ListEntriesReviewStatus] = UNSET,
    mentioned_in: Union[Unset, str] = UNSET,
    mentions: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    schema_id: Union[Unset, str] = UNSET,
    namesany_of: Union[Unset, str] = UNSET,
    namesany_ofcase_sensitive: Union[Unset, str] = UNSET,
    assigned_reviewer_idsany_of: Union[Unset, str] = UNSET,
    creator_ids: Union[Unset, str] = UNSET,
    author_idsany_of: Union[Unset, str] = UNSET,
    display_ids: Union[Unset, str] = UNSET,
    returning: Union[Unset, str] = UNSET,
) -> Response[Union[EntriesPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        sort=sort,
        name=name,
        project_id=project_id,
        review_status=review_status,
        mentioned_in=mentioned_in,
        mentions=mentions,
        ids=ids,
        schema_id=schema_id,
        namesany_of=namesany_of,
        namesany_ofcase_sensitive=namesany_ofcase_sensitive,
        assigned_reviewer_idsany_of=assigned_reviewer_idsany_of,
        creator_ids=creator_ids,
        author_idsany_of=author_idsany_of,
        display_ids=display_ids,
        returning=returning,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    sort: Union[Unset, ListEntriesSort] = ListEntriesSort.MODIFIEDAT,
    name: Union[Unset, str] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    review_status: Union[Unset, ListEntriesReviewStatus] = UNSET,
    mentioned_in: Union[Unset, str] = UNSET,
    mentions: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    schema_id: Union[Unset, str] = UNSET,
    namesany_of: Union[Unset, str] = UNSET,
    namesany_ofcase_sensitive: Union[Unset, str] = UNSET,
    assigned_reviewer_idsany_of: Union[Unset, str] = UNSET,
    creator_ids: Union[Unset, str] = UNSET,
    author_idsany_of: Union[Unset, str] = UNSET,
    display_ids: Union[Unset, str] = UNSET,
    returning: Union[Unset, str] = UNSET,
) -> Optional[Union[EntriesPaginatedList, BadRequestError]]:
    """ List notebook entries """

    return (
        await asyncio_detailed(
            client=client,
            sort=sort,
            name=name,
            project_id=project_id,
            review_status=review_status,
            mentioned_in=mentioned_in,
            mentions=mentions,
            ids=ids,
            schema_id=schema_id,
            namesany_of=namesany_of,
            namesany_ofcase_sensitive=namesany_ofcase_sensitive,
            assigned_reviewer_idsany_of=assigned_reviewer_idsany_of,
            creator_ids=creator_ids,
            author_idsany_of=author_idsany_of,
            display_ids=display_ids,
            returning=returning,
        )
    ).parsed
