import datetime
from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    owner: str,
    repo: str,
    *,
    all_: Union[Unset, str] = UNSET,
    status_types: Union[Unset, List[str]] = UNSET,
    to_status: Union[Unset, str] = UNSET,
    last_read_at: Union[Unset, datetime.datetime] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["all"] = all_

    json_status_types: Union[Unset, List[str]] = UNSET
    if not isinstance(status_types, Unset):
        json_status_types = status_types

    params["status-types"] = json_status_types

    params["to-status"] = to_status

    json_last_read_at: Union[Unset, str] = UNSET
    if not isinstance(last_read_at, Unset):
        json_last_read_at = last_read_at.isoformat()
    params["last_read_at"] = json_last_read_at

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "put",
        "url": f"/repos/{owner}/{repo}/notifications",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if response.status_code == HTTPStatus.RESET_CONTENT:
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
    all_: Union[Unset, str] = UNSET,
    status_types: Union[Unset, List[str]] = UNSET,
    to_status: Union[Unset, str] = UNSET,
    last_read_at: Union[Unset, datetime.datetime] = UNSET,
) -> Response[Any]:
    """Mark notification threads as read, pinned or unread on a specific repo

    Args:
        owner (str):
        repo (str):
        all_ (Union[Unset, str]):
        status_types (Union[Unset, List[str]]):
        to_status (Union[Unset, str]):
        last_read_at (Union[Unset, datetime.datetime]):

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
        to_status=to_status,
        last_read_at=last_read_at,
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
    all_: Union[Unset, str] = UNSET,
    status_types: Union[Unset, List[str]] = UNSET,
    to_status: Union[Unset, str] = UNSET,
    last_read_at: Union[Unset, datetime.datetime] = UNSET,
) -> Response[Any]:
    """Mark notification threads as read, pinned or unread on a specific repo

    Args:
        owner (str):
        repo (str):
        all_ (Union[Unset, str]):
        status_types (Union[Unset, List[str]]):
        to_status (Union[Unset, str]):
        last_read_at (Union[Unset, datetime.datetime]):

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
        to_status=to_status,
        last_read_at=last_read_at,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
