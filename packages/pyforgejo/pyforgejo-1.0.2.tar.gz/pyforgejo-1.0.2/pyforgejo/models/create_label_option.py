from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateLabelOption")


@_attrs_define
class CreateLabelOption:
    """CreateLabelOption options for creating a label

    Attributes:
        color (str):  Example: #00aabb.
        name (str):
        description (Union[Unset, str]):
        exclusive (Union[Unset, bool]):
        is_archived (Union[Unset, bool]):
    """

    color: str
    name: str
    description: Union[Unset, str] = UNSET
    exclusive: Union[Unset, bool] = UNSET
    is_archived: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        color = self.color

        name = self.name

        description = self.description

        exclusive = self.exclusive

        is_archived = self.is_archived

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "color": color,
                "name": name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if exclusive is not UNSET:
            field_dict["exclusive"] = exclusive
        if is_archived is not UNSET:
            field_dict["is_archived"] = is_archived

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        color = d.pop("color")

        name = d.pop("name")

        description = d.pop("description", UNSET)

        exclusive = d.pop("exclusive", UNSET)

        is_archived = d.pop("is_archived", UNSET)

        create_label_option = cls(
            color=color,
            name=name,
            description=description,
            exclusive=exclusive,
            is_archived=is_archived,
        )

        create_label_option.additional_properties = d
        return create_label_option

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
