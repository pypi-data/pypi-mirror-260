from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.automation_output_processors_paginated_list import AutomationOutputProcessorsPaginatedList
from ...models.bad_request_error import BadRequestError
from ...types import Response, UNSET, Unset


def _get_kwargs(
    *,
    client: Client,
    assay_run_id: Union[Unset, str] = UNSET,
    automation_file_config_name: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/automation-output-processors".format(client.base_url)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    params: Dict[str, Any] = {}
    if not isinstance(assay_run_id, Unset) and assay_run_id is not None:
        params["assayRunId"] = assay_run_id
    if not isinstance(automation_file_config_name, Unset) and automation_file_config_name is not None:
        params["automationFileConfigName"] = automation_file_config_name

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[AutomationOutputProcessorsPaginatedList, BadRequestError]]:
    if response.status_code == 200:
        response_200 = AutomationOutputProcessorsPaginatedList.from_dict(response.json(), strict=False)

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json(), strict=False)

        return response_400
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[AutomationOutputProcessorsPaginatedList, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    assay_run_id: Union[Unset, str] = UNSET,
    automation_file_config_name: Union[Unset, str] = UNSET,
) -> Response[Union[AutomationOutputProcessorsPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        assay_run_id=assay_run_id,
        automation_file_config_name=automation_file_config_name,
    )

    response = client.httpx_client.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    assay_run_id: Union[Unset, str] = UNSET,
    automation_file_config_name: Union[Unset, str] = UNSET,
) -> Optional[Union[AutomationOutputProcessorsPaginatedList, BadRequestError]]:
    """ List Automation Output Processors which have an attached file """

    return sync_detailed(
        client=client,
        assay_run_id=assay_run_id,
        automation_file_config_name=automation_file_config_name,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    assay_run_id: Union[Unset, str] = UNSET,
    automation_file_config_name: Union[Unset, str] = UNSET,
) -> Response[Union[AutomationOutputProcessorsPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        assay_run_id=assay_run_id,
        automation_file_config_name=automation_file_config_name,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    assay_run_id: Union[Unset, str] = UNSET,
    automation_file_config_name: Union[Unset, str] = UNSET,
) -> Optional[Union[AutomationOutputProcessorsPaginatedList, BadRequestError]]:
    """ List Automation Output Processors which have an attached file """

    return (
        await asyncio_detailed(
            client=client,
            assay_run_id=assay_run_id,
            automation_file_config_name=automation_file_config_name,
        )
    ).parsed
