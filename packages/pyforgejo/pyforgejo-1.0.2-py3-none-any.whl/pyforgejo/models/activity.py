import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.comment import Comment
    from ..models.repository import Repository
    from ..models.user import User


T = TypeVar("T", bound="Activity")


@_attrs_define
class Activity:
    """
    Attributes:
        act_user (Union[Unset, User]): User represents a user
        act_user_id (Union[Unset, int]):
        comment (Union[Unset, Comment]): Comment represents a comment on a commit or issue
        comment_id (Union[Unset, int]):
        content (Union[Unset, str]):
        created (Union[Unset, datetime.datetime]):
        id (Union[Unset, int]):
        is_private (Union[Unset, bool]):
        op_type (Union[Unset, str]):
        ref_name (Union[Unset, str]):
        repo (Union[Unset, Repository]): Repository represents a repository
        repo_id (Union[Unset, int]):
        user_id (Union[Unset, int]):
    """

    act_user: Union[Unset, "User"] = UNSET
    act_user_id: Union[Unset, int] = UNSET
    comment: Union[Unset, "Comment"] = UNSET
    comment_id: Union[Unset, int] = UNSET
    content: Union[Unset, str] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    id: Union[Unset, int] = UNSET
    is_private: Union[Unset, bool] = UNSET
    op_type: Union[Unset, str] = UNSET
    ref_name: Union[Unset, str] = UNSET
    repo: Union[Unset, "Repository"] = UNSET
    repo_id: Union[Unset, int] = UNSET
    user_id: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        act_user: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.act_user, Unset):
            act_user = self.act_user.to_dict()

        act_user_id = self.act_user_id

        comment: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.comment, Unset):
            comment = self.comment.to_dict()

        comment_id = self.comment_id

        content = self.content

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        id = self.id

        is_private = self.is_private

        op_type = self.op_type

        ref_name = self.ref_name

        repo: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.repo, Unset):
            repo = self.repo.to_dict()

        repo_id = self.repo_id

        user_id = self.user_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if act_user is not UNSET:
            field_dict["act_user"] = act_user
        if act_user_id is not UNSET:
            field_dict["act_user_id"] = act_user_id
        if comment is not UNSET:
            field_dict["comment"] = comment
        if comment_id is not UNSET:
            field_dict["comment_id"] = comment_id
        if content is not UNSET:
            field_dict["content"] = content
        if created is not UNSET:
            field_dict["created"] = created
        if id is not UNSET:
            field_dict["id"] = id
        if is_private is not UNSET:
            field_dict["is_private"] = is_private
        if op_type is not UNSET:
            field_dict["op_type"] = op_type
        if ref_name is not UNSET:
            field_dict["ref_name"] = ref_name
        if repo is not UNSET:
            field_dict["repo"] = repo
        if repo_id is not UNSET:
            field_dict["repo_id"] = repo_id
        if user_id is not UNSET:
            field_dict["user_id"] = user_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.comment import Comment
        from ..models.repository import Repository
        from ..models.user import User

        d = src_dict.copy()
        _act_user = d.pop("act_user", UNSET)
        act_user: Union[Unset, User]
        if isinstance(_act_user, Unset):
            act_user = UNSET
        else:
            act_user = User.from_dict(_act_user)

        act_user_id = d.pop("act_user_id", UNSET)

        _comment = d.pop("comment", UNSET)
        comment: Union[Unset, Comment]
        if isinstance(_comment, Unset):
            comment = UNSET
        else:
            comment = Comment.from_dict(_comment)

        comment_id = d.pop("comment_id", UNSET)

        content = d.pop("content", UNSET)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        id = d.pop("id", UNSET)

        is_private = d.pop("is_private", UNSET)

        op_type = d.pop("op_type", UNSET)

        ref_name = d.pop("ref_name", UNSET)

        _repo = d.pop("repo", UNSET)
        repo: Union[Unset, Repository]
        if isinstance(_repo, Unset):
            repo = UNSET
        else:
            repo = Repository.from_dict(_repo)

        repo_id = d.pop("repo_id", UNSET)

        user_id = d.pop("user_id", UNSET)

        activity = cls(
            act_user=act_user,
            act_user_id=act_user_id,
            comment=comment,
            comment_id=comment_id,
            content=content,
            created=created,
            id=id,
            is_private=is_private,
            op_type=op_type,
            ref_name=ref_name,
            repo=repo,
            repo_id=repo_id,
            user_id=user_id,
        )

        activity.additional_properties = d
        return activity

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
