from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.issue_config_contact_link import IssueConfigContactLink


T = TypeVar("T", bound="IssueConfig")


@_attrs_define
class IssueConfig:
    """
    Attributes:
        blank_issues_enabled (Union[Unset, bool]):
        contact_links (Union[Unset, List['IssueConfigContactLink']]):
    """

    blank_issues_enabled: Union[Unset, bool] = UNSET
    contact_links: Union[Unset, List["IssueConfigContactLink"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        blank_issues_enabled = self.blank_issues_enabled

        contact_links: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.contact_links, Unset):
            contact_links = []
            for contact_links_item_data in self.contact_links:
                contact_links_item = contact_links_item_data.to_dict()
                contact_links.append(contact_links_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if blank_issues_enabled is not UNSET:
            field_dict["blank_issues_enabled"] = blank_issues_enabled
        if contact_links is not UNSET:
            field_dict["contact_links"] = contact_links

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.issue_config_contact_link import IssueConfigContactLink

        d = src_dict.copy()
        blank_issues_enabled = d.pop("blank_issues_enabled", UNSET)

        contact_links = []
        _contact_links = d.pop("contact_links", UNSET)
        for contact_links_item_data in _contact_links or []:
            contact_links_item = IssueConfigContactLink.from_dict(contact_links_item_data)

            contact_links.append(contact_links_item)

        issue_config = cls(
            blank_issues_enabled=blank_issues_enabled,
            contact_links=contact_links,
        )

        issue_config.additional_properties = d
        return issue_config

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
