from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateBranchRepoOption")


@_attrs_define
class CreateBranchRepoOption:
    """CreateBranchRepoOption options when creating a branch in a repository

    Attributes:
        new_branch_name (str): Name of the branch to create
        old_branch_name (Union[Unset, str]): Deprecated: true
            Name of the old branch to create from
        old_ref_name (Union[Unset, str]): Name of the old branch/tag/commit to create from
    """

    new_branch_name: str
    old_branch_name: Union[Unset, str] = UNSET
    old_ref_name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        new_branch_name = self.new_branch_name

        old_branch_name = self.old_branch_name

        old_ref_name = self.old_ref_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "new_branch_name": new_branch_name,
            }
        )
        if old_branch_name is not UNSET:
            field_dict["old_branch_name"] = old_branch_name
        if old_ref_name is not UNSET:
            field_dict["old_ref_name"] = old_ref_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        new_branch_name = d.pop("new_branch_name")

        old_branch_name = d.pop("old_branch_name", UNSET)

        old_ref_name = d.pop("old_ref_name", UNSET)

        create_branch_repo_option = cls(
            new_branch_name=new_branch_name,
            old_branch_name=old_branch_name,
            old_ref_name=old_ref_name,
        )

        create_branch_repo_option.additional_properties = d
        return create_branch_repo_option

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
