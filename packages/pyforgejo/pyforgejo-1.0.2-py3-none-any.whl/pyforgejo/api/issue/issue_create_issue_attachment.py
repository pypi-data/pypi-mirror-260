import datetime
from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.issue_create_issue_attachment_body import IssueCreateIssueAttachmentBody
from ...types import UNSET, Response, Unset


def _get_kwargs(
    owner: str,
    repo: str,
    index: int,
    *,
    body: IssueCreateIssueAttachmentBody,
    name: Union[Unset, str] = UNSET,
    updated_at: Union[Unset, datetime.datetime] = UNSET,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    params: Dict[str, Any] = {}

    params["name"] = name

    json_updated_at: Union[Unset, str] = UNSET
    if not isinstance(updated_at, Unset):
        json_updated_at = updated_at.isoformat()
    params["updated_at"] = json_updated_at

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/repos/{owner}/{repo}/issues/{index}/assets",
        "params": params,
    }

    _body = body.to_multipart()

    _kwargs["files"] = _body

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if response.status_code == HTTPStatus.CREATED:
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
    index: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: IssueCreateIssueAttachmentBody,
    name: Union[Unset, str] = UNSET,
    updated_at: Union[Unset, datetime.datetime] = UNSET,
) -> Response[Any]:
    """Create an issue attachment

    Args:
        owner (str):
        repo (str):
        index (int):
        name (Union[Unset, str]):
        updated_at (Union[Unset, datetime.datetime]):
        body (IssueCreateIssueAttachmentBody):

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
        body=body,
        name=name,
        updated_at=updated_at,
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
    body: IssueCreateIssueAttachmentBody,
    name: Union[Unset, str] = UNSET,
    updated_at: Union[Unset, datetime.datetime] = UNSET,
) -> Response[Any]:
    """Create an issue attachment

    Args:
        owner (str):
        repo (str):
        index (int):
        name (Union[Unset, str]):
        updated_at (Union[Unset, datetime.datetime]):
        body (IssueCreateIssueAttachmentBody):

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
        body=body,
        name=name,
        updated_at=updated_at,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
