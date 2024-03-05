from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="NewIssuePinsAllowed")


@_attrs_define
class NewIssuePinsAllowed:
    """NewIssuePinsAllowed represents an API response that says if new Issue Pins are allowed

    Attributes:
        issues (Union[Unset, bool]):
        pull_requests (Union[Unset, bool]):
    """

    issues: Union[Unset, bool] = UNSET
    pull_requests: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        issues = self.issues

        pull_requests = self.pull_requests

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if issues is not UNSET:
            field_dict["issues"] = issues
        if pull_requests is not UNSET:
            field_dict["pull_requests"] = pull_requests

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        issues = d.pop("issues", UNSET)

        pull_requests = d.pop("pull_requests", UNSET)

        new_issue_pins_allowed = cls(
            issues=issues,
            pull_requests=pull_requests,
        )

        new_issue_pins_allowed.additional_properties = d
        return new_issue_pins_allowed

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
