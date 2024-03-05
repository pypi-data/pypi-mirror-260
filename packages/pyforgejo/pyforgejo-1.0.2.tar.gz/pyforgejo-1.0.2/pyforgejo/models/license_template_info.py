from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="LicenseTemplateInfo")


@_attrs_define
class LicenseTemplateInfo:
    """LicensesInfo contains information about a License

    Attributes:
        body (Union[Unset, str]):
        implementation (Union[Unset, str]):
        key (Union[Unset, str]):
        name (Union[Unset, str]):
        url (Union[Unset, str]):
    """

    body: Union[Unset, str] = UNSET
    implementation: Union[Unset, str] = UNSET
    key: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    url: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        body = self.body

        implementation = self.implementation

        key = self.key

        name = self.name

        url = self.url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if body is not UNSET:
            field_dict["body"] = body
        if implementation is not UNSET:
            field_dict["implementation"] = implementation
        if key is not UNSET:
            field_dict["key"] = key
        if name is not UNSET:
            field_dict["name"] = name
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        body = d.pop("body", UNSET)

        implementation = d.pop("implementation", UNSET)

        key = d.pop("key", UNSET)

        name = d.pop("name", UNSET)

        url = d.pop("url", UNSET)

        license_template_info = cls(
            body=body,
            implementation=implementation,
            key=key,
            name=name,
            url=url,
        )

        license_template_info.additional_properties = d
        return license_template_info

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
