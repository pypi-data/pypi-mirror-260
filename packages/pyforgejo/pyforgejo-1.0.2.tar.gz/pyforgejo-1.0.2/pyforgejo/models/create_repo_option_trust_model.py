from enum import Enum


class CreateRepoOptionTrustModel(str, Enum):
    COLLABORATOR = "collaborator"
    COLLABORATORCOMMITTER = "collaboratorcommitter"
    COMMITTER = "committer"
    DEFAULT = "default"

    def __str__(self) -> str:
        return str(self.value)
