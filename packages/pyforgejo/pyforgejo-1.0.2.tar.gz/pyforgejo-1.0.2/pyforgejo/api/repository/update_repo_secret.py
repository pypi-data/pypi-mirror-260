from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_or_update_secret_option import CreateOrUpdateSecretOption
from ...types import Response


def _get_kwargs(
    owner: str,
    repo: str,
    secretname: str,
    *,
    body: CreateOrUpdateSecretOption,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "put",
        "url": f"/repos/{owner}/{repo}/actions/secrets/{secretname}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if response.status_code == HTTPStatus.CREATED:
        return None
    if response.status_code == HTTPStatus.NO_CONTENT:
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
    secretname: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateOrUpdateSecretOption,
) -> Response[Any]:
    """Create or Update a secret value in a repository

    Args:
        owner (str):
        repo (str):
        secretname (str):
        body (CreateOrUpdateSecretOption): CreateOrUpdateSecretOption options when creating or
            updating secret

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        owner=owner,
        repo=repo,
        secretname=secretname,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    owner: str,
    repo: str,
    secretname: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateOrUpdateSecretOption,
) -> Response[Any]:
    """Create or Update a secret value in a repository

    Args:
        owner (str):
        repo (str):
        secretname (str):
        body (CreateOrUpdateSecretOption): CreateOrUpdateSecretOption options when creating or
            updating secret

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        owner=owner,
        repo=repo,
        secretname=secretname,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
