from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_hook_option_type import CreateHookOptionType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_hook_option_config import CreateHookOptionConfig


T = TypeVar("T", bound="CreateHookOption")


@_attrs_define
class CreateHookOption:
    """CreateHookOption options when create a hook

    Attributes:
        config (CreateHookOptionConfig): CreateHookOptionConfig has all config options in it
            required are "content_type" and "url" Required
        type (CreateHookOptionType):
        active (Union[Unset, bool]):  Default: False.
        authorization_header (Union[Unset, str]):
        branch_filter (Union[Unset, str]):
        events (Union[Unset, List[str]]):
    """

    config: "CreateHookOptionConfig"
    type: CreateHookOptionType
    active: Union[Unset, bool] = False
    authorization_header: Union[Unset, str] = UNSET
    branch_filter: Union[Unset, str] = UNSET
    events: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        config = self.config.to_dict()

        type = self.type.value

        active = self.active

        authorization_header = self.authorization_header

        branch_filter = self.branch_filter

        events: Union[Unset, List[str]] = UNSET
        if not isinstance(self.events, Unset):
            events = self.events

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "config": config,
                "type": type,
            }
        )
        if active is not UNSET:
            field_dict["active"] = active
        if authorization_header is not UNSET:
            field_dict["authorization_header"] = authorization_header
        if branch_filter is not UNSET:
            field_dict["branch_filter"] = branch_filter
        if events is not UNSET:
            field_dict["events"] = events

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_hook_option_config import CreateHookOptionConfig

        d = src_dict.copy()
        config = CreateHookOptionConfig.from_dict(d.pop("config"))

        type = CreateHookOptionType(d.pop("type"))

        active = d.pop("active", UNSET)

        authorization_header = d.pop("authorization_header", UNSET)

        branch_filter = d.pop("branch_filter", UNSET)

        events = cast(List[str], d.pop("events", UNSET))

        create_hook_option = cls(
            config=config,
            type=type,
            active=active,
            authorization_header=authorization_header,
            branch_filter=branch_filter,
            events=events,
        )

        create_hook_option.additional_properties = d
        return create_hook_option

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
