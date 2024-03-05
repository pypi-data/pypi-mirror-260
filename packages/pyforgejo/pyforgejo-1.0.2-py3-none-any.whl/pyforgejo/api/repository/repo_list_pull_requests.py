from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.repo_list_pull_requests_sort import RepoListPullRequestsSort
from ...models.repo_list_pull_requests_state import RepoListPullRequestsState
from ...types import UNSET, Response, Unset


def _get_kwargs(
    owner: str,
    repo: str,
    *,
    state: Union[Unset, RepoListPullRequestsState] = UNSET,
    sort: Union[Unset, RepoListPullRequestsSort] = UNSET,
    milestone: Union[Unset, int] = UNSET,
    labels: Union[Unset, List[int]] = UNSET,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    json_state: Union[Unset, str] = UNSET
    if not isinstance(state, Unset):
        json_state = state.value

    params["state"] = json_state

    json_sort: Union[Unset, str] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value

    params["sort"] = json_sort

    params["milestone"] = milestone

    json_labels: Union[Unset, List[int]] = UNSET
    if not isinstance(labels, Unset):
        json_labels = labels

    params["labels"] = json_labels

    params["page"] = page

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/repos/{owner}/{repo}/pulls",
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
    *,
    client: Union[AuthenticatedClient, Client],
    state: Union[Unset, RepoListPullRequestsState] = UNSET,
    sort: Union[Unset, RepoListPullRequestsSort] = UNSET,
    milestone: Union[Unset, int] = UNSET,
    labels: Union[Unset, List[int]] = UNSET,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Any]:
    """List a repo's pull requests

    Args:
        owner (str):
        repo (str):
        state (Union[Unset, RepoListPullRequestsState]):
        sort (Union[Unset, RepoListPullRequestsSort]):
        milestone (Union[Unset, int]):
        labels (Union[Unset, List[int]]):
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
        state=state,
        sort=sort,
        milestone=milestone,
        labels=labels,
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
    state: Union[Unset, RepoListPullRequestsState] = UNSET,
    sort: Union[Unset, RepoListPullRequestsSort] = UNSET,
    milestone: Union[Unset, int] = UNSET,
    labels: Union[Unset, List[int]] = UNSET,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Any]:
    """List a repo's pull requests

    Args:
        owner (str):
        repo (str):
        state (Union[Unset, RepoListPullRequestsState]):
        sort (Union[Unset, RepoListPullRequestsSort]):
        milestone (Union[Unset, int]):
        labels (Union[Unset, List[int]]):
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
        state=state,
        sort=sort,
        milestone=milestone,
        labels=labels,
        page=page,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
