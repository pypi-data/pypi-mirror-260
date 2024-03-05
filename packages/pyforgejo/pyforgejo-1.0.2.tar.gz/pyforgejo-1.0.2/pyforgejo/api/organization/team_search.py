from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.team_search_response_200 import TeamSearchResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    org: str,
    *,
    q: Union[Unset, str] = UNSET,
    include_desc: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["q"] = q

    params["include_desc"] = include_desc

    params["page"] = page

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/orgs/{org}/teams/search",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, TeamSearchResponse200]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = TeamSearchResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, TeamSearchResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    org: str,
    *,
    client: Union[AuthenticatedClient, Client],
    q: Union[Unset, str] = UNSET,
    include_desc: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Union[Any, TeamSearchResponse200]]:
    """Search for teams within an organization

    Args:
        org (str):
        q (Union[Unset, str]):
        include_desc (Union[Unset, bool]):
        page (Union[Unset, int]):
        limit (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, TeamSearchResponse200]]
    """

    kwargs = _get_kwargs(
        org=org,
        q=q,
        include_desc=include_desc,
        page=page,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org: str,
    *,
    client: Union[AuthenticatedClient, Client],
    q: Union[Unset, str] = UNSET,
    include_desc: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Optional[Union[Any, TeamSearchResponse200]]:
    """Search for teams within an organization

    Args:
        org (str):
        q (Union[Unset, str]):
        include_desc (Union[Unset, bool]):
        page (Union[Unset, int]):
        limit (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, TeamSearchResponse200]
    """

    return sync_detailed(
        org=org,
        client=client,
        q=q,
        include_desc=include_desc,
        page=page,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    org: str,
    *,
    client: Union[AuthenticatedClient, Client],
    q: Union[Unset, str] = UNSET,
    include_desc: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Union[Any, TeamSearchResponse200]]:
    """Search for teams within an organization

    Args:
        org (str):
        q (Union[Unset, str]):
        include_desc (Union[Unset, bool]):
        page (Union[Unset, int]):
        limit (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, TeamSearchResponse200]]
    """

    kwargs = _get_kwargs(
        org=org,
        q=q,
        include_desc=include_desc,
        page=page,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org: str,
    *,
    client: Union[AuthenticatedClient, Client],
    q: Union[Unset, str] = UNSET,
    include_desc: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Optional[Union[Any, TeamSearchResponse200]]:
    """Search for teams within an organization

    Args:
        org (str):
        q (Union[Unset, str]):
        include_desc (Union[Unset, bool]):
        page (Union[Unset, int]):
        limit (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, TeamSearchResponse200]
    """

    return (
        await asyncio_detailed(
            org=org,
            client=client,
            q=q,
            include_desc=include_desc,
            page=page,
            limit=limit,
        )
    ).parsed
