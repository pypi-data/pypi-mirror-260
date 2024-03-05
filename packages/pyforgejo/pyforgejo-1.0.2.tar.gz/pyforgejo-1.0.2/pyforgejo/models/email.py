from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Email")


@_attrs_define
class Email:
    """Email an email address belonging to a user

    Attributes:
        email (Union[Unset, str]):
        primary (Union[Unset, bool]):
        user_id (Union[Unset, int]):
        username (Union[Unset, str]):
        verified (Union[Unset, bool]):
    """

    email: Union[Unset, str] = UNSET
    primary: Union[Unset, bool] = UNSET
    user_id: Union[Unset, int] = UNSET
    username: Union[Unset, str] = UNSET
    verified: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        email = self.email

        primary = self.primary

        user_id = self.user_id

        username = self.username

        verified = self.verified

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if email is not UNSET:
            field_dict["email"] = email
        if primary is not UNSET:
            field_dict["primary"] = primary
        if user_id is not UNSET:
            field_dict["user_id"] = user_id
        if username is not UNSET:
            field_dict["username"] = username
        if verified is not UNSET:
            field_dict["verified"] = verified

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        email = d.pop("email", UNSET)

        primary = d.pop("primary", UNSET)

        user_id = d.pop("user_id", UNSET)

        username = d.pop("username", UNSET)

        verified = d.pop("verified", UNSET)

        email = cls(
            email=email,
            primary=primary,
            user_id=user_id,
            username=username,
            verified=verified,
        )

        email.additional_properties = d
        return email

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
