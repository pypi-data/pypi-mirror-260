from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    owner: str,
    repo: str,
    *,
    sha: Union[Unset, str] = UNSET,
    path: Union[Unset, str] = UNSET,
    stat: Union[Unset, bool] = UNSET,
    verification: Union[Unset, bool] = UNSET,
    files: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    not_: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["sha"] = sha

    params["path"] = path

    params["stat"] = stat

    params["verification"] = verification

    params["files"] = files

    params["page"] = page

    params["limit"] = limit

    params["not"] = not_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/repos/{owner}/{repo}/commits",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if response.status_code == HTTPStatus.OK:
        return None
    if response.status_code == HTTPStatus.NOT_FOUND:
        return None
    if response.status_code == HTTPStatus.CONFLICT:
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
    sha: Union[Unset, str] = UNSET,
    path: Union[Unset, str] = UNSET,
    stat: Union[Unset, bool] = UNSET,
    verification: Union[Unset, bool] = UNSET,
    files: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    not_: Union[Unset, str] = UNSET,
) -> Response[Any]:
    """Get a list of all commits from a repository

    Args:
        owner (str):
        repo (str):
        sha (Union[Unset, str]):
        path (Union[Unset, str]):
        stat (Union[Unset, bool]):
        verification (Union[Unset, bool]):
        files (Union[Unset, bool]):
        page (Union[Unset, int]):
        limit (Union[Unset, int]):
        not_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        owner=owner,
        repo=repo,
        sha=sha,
        path=path,
        stat=stat,
        verification=verification,
        files=files,
        page=page,
        limit=limit,
        not_=not_,
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
    sha: Union[Unset, str] = UNSET,
    path: Union[Unset, str] = UNSET,
    stat: Union[Unset, bool] = UNSET,
    verification: Union[Unset, bool] = UNSET,
    files: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    not_: Union[Unset, str] = UNSET,
) -> Response[Any]:
    """Get a list of all commits from a repository

    Args:
        owner (str):
        repo (str):
        sha (Union[Unset, str]):
        path (Union[Unset, str]):
        stat (Union[Unset, bool]):
        verification (Union[Unset, bool]):
        files (Union[Unset, bool]):
        page (Union[Unset, int]):
        limit (Union[Unset, int]):
        not_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        owner=owner,
        repo=repo,
        sha=sha,
        path=path,
        stat=stat,
        verification=verification,
        files=files,
        page=page,
        limit=limit,
        not_=not_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
