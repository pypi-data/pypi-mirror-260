from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MarkupOption")


@_attrs_define
class MarkupOption:
    """MarkupOption markup options

    Attributes:
        context (Union[Unset, str]): Context to render

            in: body
        file_path (Union[Unset, str]): File path for detecting extension in file mode

            in: body
        mode (Union[Unset, str]): Mode to render (comment, gfm, markdown, file)

            in: body
        text (Union[Unset, str]): Text markup to render

            in: body
        wiki (Union[Unset, bool]): Is it a wiki page ?

            in: body
    """

    context: Union[Unset, str] = UNSET
    file_path: Union[Unset, str] = UNSET
    mode: Union[Unset, str] = UNSET
    text: Union[Unset, str] = UNSET
    wiki: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        context = self.context

        file_path = self.file_path

        mode = self.mode

        text = self.text

        wiki = self.wiki

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if context is not UNSET:
            field_dict["Context"] = context
        if file_path is not UNSET:
            field_dict["FilePath"] = file_path
        if mode is not UNSET:
            field_dict["Mode"] = mode
        if text is not UNSET:
            field_dict["Text"] = text
        if wiki is not UNSET:
            field_dict["Wiki"] = wiki

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        context = d.pop("Context", UNSET)

        file_path = d.pop("FilePath", UNSET)

        mode = d.pop("Mode", UNSET)

        text = d.pop("Text", UNSET)

        wiki = d.pop("Wiki", UNSET)

        markup_option = cls(
            context=context,
            file_path=file_path,
            mode=mode,
            text=text,
            wiki=wiki,
        )

        markup_option.additional_properties = d
        return markup_option

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
