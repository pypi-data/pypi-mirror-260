from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.change_file_operation_operation import ChangeFileOperationOperation
from ..types import UNSET, Unset

T = TypeVar("T", bound="ChangeFileOperation")


@_attrs_define
class ChangeFileOperation:
    """ChangeFileOperation for creating, updating or deleting a file

    Attributes:
        operation (ChangeFileOperationOperation): indicates what to do with the file
        path (str): path to the existing or new file
        content (Union[Unset, str]): new or updated file content, must be base64 encoded
        from_path (Union[Unset, str]): old path of the file to move
        sha (Union[Unset, str]): sha is the SHA for the file that already exists, required for update or delete
    """

    operation: ChangeFileOperationOperation
    path: str
    content: Union[Unset, str] = UNSET
    from_path: Union[Unset, str] = UNSET
    sha: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        operation = self.operation.value

        path = self.path

        content = self.content

        from_path = self.from_path

        sha = self.sha

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "operation": operation,
                "path": path,
            }
        )
        if content is not UNSET:
            field_dict["content"] = content
        if from_path is not UNSET:
            field_dict["from_path"] = from_path
        if sha is not UNSET:
            field_dict["sha"] = sha

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        operation = ChangeFileOperationOperation(d.pop("operation"))

        path = d.pop("path")

        content = d.pop("content", UNSET)

        from_path = d.pop("from_path", UNSET)

        sha = d.pop("sha", UNSET)

        change_file_operation = cls(
            operation=operation,
            path=path,
            content=content,
            from_path=from_path,
            sha=sha,
        )

        change_file_operation.additional_properties = d
        return change_file_operation

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
