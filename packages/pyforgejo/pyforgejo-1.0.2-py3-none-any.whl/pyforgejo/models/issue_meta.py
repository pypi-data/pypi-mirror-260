from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="IssueMeta")


@_attrs_define
class IssueMeta:
    """IssueMeta basic issue information

    Attributes:
        index (Union[Unset, int]):
        owner (Union[Unset, str]):
        repo (Union[Unset, str]):
    """

    index: Union[Unset, int] = UNSET
    owner: Union[Unset, str] = UNSET
    repo: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        index = self.index

        owner = self.owner

        repo = self.repo

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if index is not UNSET:
            field_dict["index"] = index
        if owner is not UNSET:
            field_dict["owner"] = owner
        if repo is not UNSET:
            field_dict["repo"] = repo

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        index = d.pop("index", UNSET)

        owner = d.pop("owner", UNSET)

        repo = d.pop("repo", UNSET)

        issue_meta = cls(
            index=index,
            owner=owner,
            repo=repo,
        )

        issue_meta.additional_properties = d
        return issue_meta

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
