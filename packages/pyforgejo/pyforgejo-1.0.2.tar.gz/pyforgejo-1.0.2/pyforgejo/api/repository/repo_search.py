from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    q: Union[Unset, str] = UNSET,
    topic: Union[Unset, bool] = UNSET,
    include_desc: Union[Unset, bool] = UNSET,
    uid: Union[Unset, int] = UNSET,
    priority_owner_id: Union[Unset, int] = UNSET,
    team_id: Union[Unset, int] = UNSET,
    starred_by: Union[Unset, int] = UNSET,
    private: Union[Unset, bool] = UNSET,
    is_private: Union[Unset, bool] = UNSET,
    template: Union[Unset, bool] = UNSET,
    archived: Union[Unset, bool] = UNSET,
    mode: Union[Unset, str] = UNSET,
    exclusive: Union[Unset, bool] = UNSET,
    sort: Union[Unset, str] = UNSET,
    order: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["q"] = q

    params["topic"] = topic

    params["includeDesc"] = include_desc

    params["uid"] = uid

    params["priority_owner_id"] = priority_owner_id

    params["team_id"] = team_id

    params["starredBy"] = starred_by

    params["private"] = private

    params["is_private"] = is_private

    params["template"] = template

    params["archived"] = archived

    params["mode"] = mode

    params["exclusive"] = exclusive

    params["sort"] = sort

    params["order"] = order

    params["page"] = page

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/repos/search",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if response.status_code == HTTPStatus.OK:
        return None
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
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
    q: Union[Unset, str] = UNSET,
    topic: Union[Unset, bool] = UNSET,
    include_desc: Union[Unset, bool] = UNSET,
    uid: Union[Unset, int] = UNSET,
    priority_owner_id: Union[Unset, int] = UNSET,
    team_id: Union[Unset, int] = UNSET,
    starred_by: Union[Unset, int] = UNSET,
    private: Union[Unset, bool] = UNSET,
    is_private: Union[Unset, bool] = UNSET,
    template: Union[Unset, bool] = UNSET,
    archived: Union[Unset, bool] = UNSET,
    mode: Union[Unset, str] = UNSET,
    exclusive: Union[Unset, bool] = UNSET,
    sort: Union[Unset, str] = UNSET,
    order: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Any]:
    """Search for repositories

    Args:
        q (Union[Unset, str]):
        topic (Union[Unset, bool]):
        include_desc (Union[Unset, bool]):
        uid (Union[Unset, int]):
        priority_owner_id (Union[Unset, int]):
        team_id (Union[Unset, int]):
        starred_by (Union[Unset, int]):
        private (Union[Unset, bool]):
        is_private (Union[Unset, bool]):
        template (Union[Unset, bool]):
        archived (Union[Unset, bool]):
        mode (Union[Unset, str]):
        exclusive (Union[Unset, bool]):
        sort (Union[Unset, str]):
        order (Union[Unset, str]):
        page (Union[Unset, int]):
        limit (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        q=q,
        topic=topic,
        include_desc=include_desc,
        uid=uid,
        priority_owner_id=priority_owner_id,
        team_id=team_id,
        starred_by=starred_by,
        private=private,
        is_private=is_private,
        template=template,
        archived=archived,
        mode=mode,
        exclusive=exclusive,
        sort=sort,
        order=order,
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
    q: Union[Unset, str] = UNSET,
    topic: Union[Unset, bool] = UNSET,
    include_desc: Union[Unset, bool] = UNSET,
    uid: Union[Unset, int] = UNSET,
    priority_owner_id: Union[Unset, int] = UNSET,
    team_id: Union[Unset, int] = UNSET,
    starred_by: Union[Unset, int] = UNSET,
    private: Union[Unset, bool] = UNSET,
    is_private: Union[Unset, bool] = UNSET,
    template: Union[Unset, bool] = UNSET,
    archived: Union[Unset, bool] = UNSET,
    mode: Union[Unset, str] = UNSET,
    exclusive: Union[Unset, bool] = UNSET,
    sort: Union[Unset, str] = UNSET,
    order: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Any]:
    """Search for repositories

    Args:
        q (Union[Unset, str]):
        topic (Union[Unset, bool]):
        include_desc (Union[Unset, bool]):
        uid (Union[Unset, int]):
        priority_owner_id (Union[Unset, int]):
        team_id (Union[Unset, int]):
        starred_by (Union[Unset, int]):
        private (Union[Unset, bool]):
        is_private (Union[Unset, bool]):
        template (Union[Unset, bool]):
        archived (Union[Unset, bool]):
        mode (Union[Unset, str]):
        exclusive (Union[Unset, bool]):
        sort (Union[Unset, str]):
        order (Union[Unset, str]):
        page (Union[Unset, int]):
        limit (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        q=q,
        topic=topic,
        include_desc=include_desc,
        uid=uid,
        priority_owner_id=priority_owner_id,
        team_id=team_id,
        starred_by=starred_by,
        private=private,
        is_private=is_private,
        template=template,
        archived=archived,
        mode=mode,
        exclusive=exclusive,
        sort=sort,
        order=order,
        page=page,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
