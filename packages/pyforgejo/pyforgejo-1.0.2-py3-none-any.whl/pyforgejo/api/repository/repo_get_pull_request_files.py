from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.repo_get_pull_request_files_whitespace import RepoGetPullRequestFilesWhitespace
from ...types import UNSET, Response, Unset


def _get_kwargs(
    owner: str,
    repo: str,
    index: int,
    *,
    skip_to: Union[Unset, str] = UNSET,
    whitespace: Union[Unset, RepoGetPullRequestFilesWhitespace] = UNSET,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["skip-to"] = skip_to

    json_whitespace: Union[Unset, str] = UNSET
    if not isinstance(whitespace, Unset):
        json_whitespace = whitespace.value

    params["whitespace"] = json_whitespace

    params["page"] = page

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/repos/{owner}/{repo}/pulls/{index}/files",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if response.status_code == HTTPStatus.OK:
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
    index: int,
    *,
    client: Union[AuthenticatedClient, Client],
    skip_to: Union[Unset, str] = UNSET,
    whitespace: Union[Unset, RepoGetPullRequestFilesWhitespace] = UNSET,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Any]:
    """Get changed files for a pull request

    Args:
        owner (str):
        repo (str):
        index (int):
        skip_to (Union[Unset, str]):
        whitespace (Union[Unset, RepoGetPullRequestFilesWhitespace]):
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
        index=index,
        skip_to=skip_to,
        whitespace=whitespace,
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
    index: int,
    *,
    client: Union[AuthenticatedClient, Client],
    skip_to: Union[Unset, str] = UNSET,
    whitespace: Union[Unset, RepoGetPullRequestFilesWhitespace] = UNSET,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Any]:
    """Get changed files for a pull request

    Args:
        owner (str):
        repo (str):
        index (int):
        skip_to (Union[Unset, str]):
        whitespace (Union[Unset, RepoGetPullRequestFilesWhitespace]):
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
        index=index,
        skip_to=skip_to,
        whitespace=whitespace,
        page=page,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
