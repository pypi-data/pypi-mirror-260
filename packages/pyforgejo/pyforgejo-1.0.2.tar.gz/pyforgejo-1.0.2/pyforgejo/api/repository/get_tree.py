from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    owner: str,
    repo: str,
    sha: str,
    *,
    recursive: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    per_page: Union[Unset, int] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["recursive"] = recursive

    params["page"] = page

    params["per_page"] = per_page

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/repos/{owner}/{repo}/git/trees/{sha}",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if response.status_code == HTTPStatus.OK:
        return None
    if response.status_code == HTTPStatus.BAD_REQUEST:
        return None
    if response.status_code == HTTPStatus.NOT_FOUND:
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
    sha: str,
    *,
    client: Union[AuthenticatedClient, Client],
    recursive: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    per_page: Union[Unset, int] = UNSET,
) -> Response[Any]:
    """Gets the tree of a repository.

    Args:
        owner (str):
        repo (str):
        sha (str):
        recursive (Union[Unset, bool]):
        page (Union[Unset, int]):
        per_page (Union[Unset, int]):

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
        recursive=recursive,
        page=page,
        per_page=per_page,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    owner: str,
    repo: str,
    sha: str,
    *,
    client: Union[AuthenticatedClient, Client],
    recursive: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    per_page: Union[Unset, int] = UNSET,
) -> Response[Any]:
    """Gets the tree of a repository.

    Args:
        owner (str):
        repo (str):
        sha (str):
        recursive (Union[Unset, bool]):
        page (Union[Unset, int]):
        per_page (Union[Unset, int]):

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
        recursive=recursive,
        page=page,
        per_page=per_page,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
