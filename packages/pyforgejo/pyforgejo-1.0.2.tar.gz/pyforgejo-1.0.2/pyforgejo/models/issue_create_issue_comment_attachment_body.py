from io import BytesIO
from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import File

T = TypeVar("T", bound="IssueCreateIssueCommentAttachmentBody")


@_attrs_define
class IssueCreateIssueCommentAttachmentBody:
    """
    Attributes:
        attachment (File): attachment to upload
    """

    attachment: File
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        attachment = self.attachment.to_tuple()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "attachment": attachment,
            }
        )

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        attachment = self.attachment.to_tuple()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {key: (None, str(value).encode(), "text/plain") for key, value in self.additional_properties.items()}
        )
        field_dict.update(
            {
                "attachment": attachment,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        attachment = File(payload=BytesIO(d.pop("attachment")))

        issue_create_issue_comment_attachment_body = cls(
            attachment=attachment,
        )

        issue_create_issue_comment_attachment_body.additional_properties = d
        return issue_create_issue_comment_attachment_body

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
