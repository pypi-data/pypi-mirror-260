from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Label")


@_attrs_define
class Label:
    """Label a label to an issue or a pr

    Attributes:
        color (Union[Unset, str]):  Example: 00aabb.
        description (Union[Unset, str]):
        exclusive (Union[Unset, bool]):
        id (Union[Unset, int]):
        is_archived (Union[Unset, bool]):
        name (Union[Unset, str]):
        url (Union[Unset, str]):
    """

    color: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    exclusive: Union[Unset, bool] = UNSET
    id: Union[Unset, int] = UNSET
    is_archived: Union[Unset, bool] = UNSET
    name: Union[Unset, str] = UNSET
    url: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        color = self.color

        description = self.description

        exclusive = self.exclusive

        id = self.id

        is_archived = self.is_archived

        name = self.name

        url = self.url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if color is not UNSET:
            field_dict["color"] = color
        if description is not UNSET:
            field_dict["description"] = description
        if exclusive is not UNSET:
            field_dict["exclusive"] = exclusive
        if id is not UNSET:
            field_dict["id"] = id
        if is_archived is not UNSET:
            field_dict["is_archived"] = is_archived
        if name is not UNSET:
            field_dict["name"] = name
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        color = d.pop("color", UNSET)

        description = d.pop("description", UNSET)

        exclusive = d.pop("exclusive", UNSET)

        id = d.pop("id", UNSET)

        is_archived = d.pop("is_archived", UNSET)

        name = d.pop("name", UNSET)

        url = d.pop("url", UNSET)

        label = cls(
            color=color,
            description=description,
            exclusive=exclusive,
            id=id,
            is_archived=is_archived,
            name=name,
            url=url,
        )

        label.additional_properties = d
        return label

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
