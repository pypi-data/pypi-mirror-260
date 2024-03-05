import datetime
from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.notify_get_repo_list_subject_type_item import NotifyGetRepoListSubjectTypeItem
from ...types import UNSET, Response, Unset


def _get_kwargs(
    owner: str,
    repo: str,
    *,
    all_: Union[Unset, bool] = UNSET,
    status_types: Union[Unset, List[str]] = UNSET,
    subject_type: Union[Unset, List[NotifyGetRepoListSubjectTypeItem]] = UNSET,
    since: Union[Unset, datetime.datetime] = UNSET,
    before: Union[Unset, datetime.datetime] = UNSET,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["all"] = all_

    json_status_types: Union[Unset, List[str]] = UNSET
    if not isinstance(status_types, Unset):
        json_status_types = status_types

    params["status-types"] = json_status_types

    json_subject_type: Union[Unset, List[str]] = UNSET
    if not isinstance(subject_type, Unset):
        json_subject_type = []
        for subject_type_item_data in subject_type:
            subject_type_item = subject_type_item_data.value
            json_subject_type.append(subject_type_item)

    params["subject-type"] = json_subject_type

    json_since: Union[Unset, str] = UNSET
    if not isinstance(since, Unset):
        json_since = since.isoformat()
    params["since"] = json_since

    json_before: Union[Unset, str] = UNSET
    if not isinstance(before, Unset):
        json_before = before.isoformat()
    params["before"] = json_before

    params["page"] = page

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/repos/{owner}/{repo}/notifications",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if response.status_code == HTTPStatus.OK:
        return None
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    owner: str,
    repo: str,
    *,
    client: Union[AuthenticatedClient, Client],
    all_: Union[Unset, bool] = UNSET,
    status_types: Union[Unset, List[str]] = UNSET,
    subject_type: Union[Unset, List[NotifyGetRepoListSubjectTypeItem]] = UNSET,
    since: Union[Unset, datetime.datetime] = UNSET,
    before: Union[Unset, datetime.datetime] = UNSET,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Any]:
    """List users's notification threads on a specific repo

    Args:
        owner (str):
        repo (str):
        all_ (Union[Unset, bool]):
        status_types (Union[Unset, List[str]]):
        subject_type (Union[Unset, List[NotifyGetRepoListSubjectTypeItem]]):
        since (Union[Unset, datetime.datetime]):
        before (Union[Unset, datetime.datetime]):
        page (Union[Unset, int]):
        limit (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        owner=owner,
        repo=repo,
        all_=all_,
        status_types=status_types,
        subject_type=subject_type,
        since=since,
        before=before,
        page=page,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    owner: str,
    repo: str,
    *,
    client: Union[AuthenticatedClient, Client],
    all_: Union[Unset, bool] = UNSET,
    status_types: Union[Unset, List[str]] = UNSET,
    subject_type: Union[Unset, List[NotifyGetRepoListSubjectTypeItem]] = UNSET,
    since: Union[Unset, datetime.datetime] = UNSET,
    before: Union[Unset, datetime.datetime] = UNSET,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Any]:
    """List users's notification threads on a specific repo

    Args:
        owner (str):
        repo (str):
        all_ (Union[Unset, bool]):
        status_types (Union[Unset, List[str]]):
        subject_type (Union[Unset, List[NotifyGetRepoListSubjectTypeItem]]):
        since (Union[Unset, datetime.datetime]):
        before (Union[Unset, datetime.datetime]):
        page (Union[Unset, int]):
        limit (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        owner=owner,
        repo=repo,
        all_=all_,
        status_types=status_types,
        subject_type=subject_type,
        since=since,
        before=before,
        page=page,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
