from enum import Enum


class NotifyGetRepoListSubjectTypeItem(str, Enum):
    COMMIT = "commit"
    ISSUE = "issue"
    PULL = "pull"
    REPOSITORY = "repository"

    def __str__(self) -> str:
        return str(self.value)
