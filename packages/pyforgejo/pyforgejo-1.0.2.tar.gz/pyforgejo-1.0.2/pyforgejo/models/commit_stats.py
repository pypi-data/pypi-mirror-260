from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CommitStats")


@_attrs_define
class CommitStats:
    """CommitStats is statistics for a RepoCommit

    Attributes:
        additions (Union[Unset, int]):
        deletions (Union[Unset, int]):
        total (Union[Unset, int]):
    """

    additions: Union[Unset, int] = UNSET
    deletions: Union[Unset, int] = UNSET
    total: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        additions = self.additions

        deletions = self.deletions

        total = self.total

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if additions is not UNSET:
            field_dict["additions"] = additions
        if deletions is not UNSET:
            field_dict["deletions"] = deletions
        if total is not UNSET:
            field_dict["total"] = total

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        additions = d.pop("additions", UNSET)

        deletions = d.pop("deletions", UNSET)

        total = d.pop("total", UNSET)

        commit_stats = cls(
            additions=additions,
            deletions=deletions,
            total=total,
        )

        commit_stats.additional_properties = d
        return commit_stats

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
