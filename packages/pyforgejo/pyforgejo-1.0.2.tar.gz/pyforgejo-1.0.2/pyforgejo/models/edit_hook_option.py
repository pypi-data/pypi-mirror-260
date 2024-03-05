from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.edit_hook_option_config import EditHookOptionConfig


T = TypeVar("T", bound="EditHookOption")


@_attrs_define
class EditHookOption:
    """EditHookOption options when modify one hook

    Attributes:
        active (Union[Unset, bool]):
        authorization_header (Union[Unset, str]):
        branch_filter (Union[Unset, str]):
        config (Union[Unset, EditHookOptionConfig]):
        events (Union[Unset, List[str]]):
    """

    active: Union[Unset, bool] = UNSET
    authorization_header: Union[Unset, str] = UNSET
    branch_filter: Union[Unset, str] = UNSET
    config: Union[Unset, "EditHookOptionConfig"] = UNSET
    events: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        active = self.active

        authorization_header = self.authorization_header

        branch_filter = self.branch_filter

        config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        events: Union[Unset, List[str]] = UNSET
        if not isinstance(self.events, Unset):
            events = self.events

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if active is not UNSET:
            field_dict["active"] = active
        if authorization_header is not UNSET:
            field_dict["authorization_header"] = authorization_header
        if branch_filter is not UNSET:
            field_dict["branch_filter"] = branch_filter
        if config is not UNSET:
            field_dict["config"] = config
        if events is not UNSET:
            field_dict["events"] = events

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.edit_hook_option_config import EditHookOptionConfig

        d = src_dict.copy()
        active = d.pop("active", UNSET)

        authorization_header = d.pop("authorization_header", UNSET)

        branch_filter = d.pop("branch_filter", UNSET)

        _config = d.pop("config", UNSET)
        config: Union[Unset, EditHookOptionConfig]
        if isinstance(_config, Unset):
            config = UNSET
        else:
            config = EditHookOptionConfig.from_dict(_config)

        events = cast(List[str], d.pop("events", UNSET))

        edit_hook_option = cls(
            active=active,
            authorization_header=authorization_header,
            branch_filter=branch_filter,
            config=config,
            events=events,
        )

        edit_hook_option.additional_properties = d
        return edit_hook_option

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
