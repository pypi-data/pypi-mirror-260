import datetime
from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    state: Union[Unset, str] = UNSET,
    labels: Union[Unset, str] = UNSET,
    milestones: Union[Unset, str] = UNSET,
    q: Union[Unset, str] = UNSET,
    priority_repo_id: Union[Unset, int] = UNSET,
    type: Union[Unset, str] = UNSET,
    since: Union[Unset, datetime.datetime] = UNSET,
    before: Union[Unset, datetime.datetime] = UNSET,
    assigned: Union[Unset, bool] = UNSET,
    created: Union[Unset, bool] = UNSET,
    mentioned: Union[Unset, bool] = UNSET,
    review_requested: Union[Unset, bool] = UNSET,
    reviewed: Union[Unset, bool] = UNSET,
    owner: Union[Unset, str] = UNSET,
    team: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["state"] = state

    params["labels"] = labels

    params["milestones"] = milestones

    params["q"] = q

    params["priority_repo_id"] = priority_repo_id

    params["type"] = type

    json_since: Union[Unset, str] = UNSET
    if not isinstance(since, Unset):
        json_since = since.isoformat()
    params["since"] = json_since

    json_before: Union[Unset, str] = UNSET
    if not isinstance(before, Unset):
        json_before = before.isoformat()
    params["before"] = json_before

    params["assigned"] = assigned

    params["created"] = created

    params["mentioned"] = mentioned

    params["review_requested"] = review_requested

    params["reviewed"] = reviewed

    params["owner"] = owner

    params["team"] = team

    params["page"] = page

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/repos/issues/search",
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
    *,
    client: Union[AuthenticatedClient, Client],
    state: Union[Unset, str] = UNSET,
    labels: Union[Unset, str] = UNSET,
    milestones: Union[Unset, str] = UNSET,
    q: Union[Unset, str] = UNSET,
    priority_repo_id: Union[Unset, int] = UNSET,
    type: Union[Unset, str] = UNSET,
    since: Union[Unset, datetime.datetime] = UNSET,
    before: Union[Unset, datetime.datetime] = UNSET,
    assigned: Union[Unset, bool] = UNSET,
    created: Union[Unset, bool] = UNSET,
    mentioned: Union[Unset, bool] = UNSET,
    review_requested: Union[Unset, bool] = UNSET,
    reviewed: Union[Unset, bool] = UNSET,
    owner: Union[Unset, str] = UNSET,
    team: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Any]:
    """Search for issues across the repositories that the user has access to

    Args:
        state (Union[Unset, str]):
        labels (Union[Unset, str]):
        milestones (Union[Unset, str]):
        q (Union[Unset, str]):
        priority_repo_id (Union[Unset, int]):
        type (Union[Unset, str]):
        since (Union[Unset, datetime.datetime]):
        before (Union[Unset, datetime.datetime]):
        assigned (Union[Unset, bool]):
        created (Union[Unset, bool]):
        mentioned (Union[Unset, bool]):
        review_requested (Union[Unset, bool]):
        reviewed (Union[Unset, bool]):
        owner (Union[Unset, str]):
        team (Union[Unset, str]):
        page (Union[Unset, int]):
        limit (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        state=state,
        labels=labels,
        milestones=milestones,
        q=q,
        priority_repo_id=priority_repo_id,
        type=type,
        since=since,
        before=before,
        assigned=assigned,
        created=created,
        mentioned=mentioned,
        review_requested=review_requested,
        reviewed=reviewed,
        owner=owner,
        team=team,
        page=page,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    state: Union[Unset, str] = UNSET,
    labels: Union[Unset, str] = UNSET,
    milestones: Union[Unset, str] = UNSET,
    q: Union[Unset, str] = UNSET,
    priority_repo_id: Union[Unset, int] = UNSET,
    type: Union[Unset, str] = UNSET,
    since: Union[Unset, datetime.datetime] = UNSET,
    before: Union[Unset, datetime.datetime] = UNSET,
    assigned: Union[Unset, bool] = UNSET,
    created: Union[Unset, bool] = UNSET,
    mentioned: Union[Unset, bool] = UNSET,
    review_requested: Union[Unset, bool] = UNSET,
    reviewed: Union[Unset, bool] = UNSET,
    owner: Union[Unset, str] = UNSET,
    team: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Any]:
    """Search for issues across the repositories that the user has access to

    Args:
        state (Union[Unset, str]):
        labels (Union[Unset, str]):
        milestones (Union[Unset, str]):
        q (Union[Unset, str]):
        priority_repo_id (Union[Unset, int]):
        type (Union[Unset, str]):
        since (Union[Unset, datetime.datetime]):
        before (Union[Unset, datetime.datetime]):
        assigned (Union[Unset, bool]):
        created (Union[Unset, bool]):
        mentioned (Union[Unset, bool]):
        review_requested (Union[Unset, bool]):
        reviewed (Union[Unset, bool]):
        owner (Union[Unset, str]):
        team (Union[Unset, str]):
        page (Union[Unset, int]):
        limit (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        state=state,
        labels=labels,
        milestones=milestones,
        q=q,
        priority_repo_id=priority_repo_id,
        type=type,
        since=since,
        before=before,
        assigned=assigned,
        created=created,
        mentioned=mentioned,
        review_requested=review_requested,
        reviewed=reviewed,
        owner=owner,
        team=team,
        page=page,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
