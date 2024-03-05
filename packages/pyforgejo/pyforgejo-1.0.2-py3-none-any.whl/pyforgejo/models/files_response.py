from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.contents_response import ContentsResponse
    from ..models.file_commit_response_contains_information_generated_from_a_git_commit_for_a_repos_file import (
        FileCommitResponseContainsInformationGeneratedFromAGitCommitForAReposFile,
    )
    from ..models.payload_commit_verification import PayloadCommitVerification


T = TypeVar("T", bound="FilesResponse")


@_attrs_define
class FilesResponse:
    """FilesResponse contains information about multiple files from a repo

    Attributes:
        commit (Union[Unset, FileCommitResponseContainsInformationGeneratedFromAGitCommitForAReposFile]):
        files (Union[Unset, List['ContentsResponse']]):
        verification (Union[Unset, PayloadCommitVerification]): PayloadCommitVerification represents the GPG
            verification of a commit
    """

    commit: Union[Unset, "FileCommitResponseContainsInformationGeneratedFromAGitCommitForAReposFile"] = UNSET
    files: Union[Unset, List["ContentsResponse"]] = UNSET
    verification: Union[Unset, "PayloadCommitVerification"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        commit: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.commit, Unset):
            commit = self.commit.to_dict()

        files: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.files, Unset):
            files = []
            for files_item_data in self.files:
                files_item = files_item_data.to_dict()
                files.append(files_item)

        verification: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.verification, Unset):
            verification = self.verification.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if commit is not UNSET:
            field_dict["commit"] = commit
        if files is not UNSET:
            field_dict["files"] = files
        if verification is not UNSET:
            field_dict["verification"] = verification

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.contents_response import ContentsResponse
        from ..models.file_commit_response_contains_information_generated_from_a_git_commit_for_a_repos_file import (
            FileCommitResponseContainsInformationGeneratedFromAGitCommitForAReposFile,
        )
        from ..models.payload_commit_verification import PayloadCommitVerification

        d = src_dict.copy()
        _commit = d.pop("commit", UNSET)
        commit: Union[Unset, FileCommitResponseContainsInformationGeneratedFromAGitCommitForAReposFile]
        if isinstance(_commit, Unset):
            commit = UNSET
        else:
            commit = FileCommitResponseContainsInformationGeneratedFromAGitCommitForAReposFile.from_dict(_commit)

        files = []
        _files = d.pop("files", UNSET)
        for files_item_data in _files or []:
            files_item = ContentsResponse.from_dict(files_item_data)

            files.append(files_item)

        _verification = d.pop("verification", UNSET)
        verification: Union[Unset, PayloadCommitVerification]
        if isinstance(_verification, Unset):
            verification = UNSET
        else:
            verification = PayloadCommitVerification.from_dict(_verification)

        files_response = cls(
            commit=commit,
            files=files,
            verification=verification,
        )

        files_response.additional_properties = d
        return files_response

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
