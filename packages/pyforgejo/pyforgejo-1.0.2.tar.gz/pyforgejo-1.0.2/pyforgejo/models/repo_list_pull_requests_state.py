from enum import Enum


class RepoListPullRequestsState(str, Enum):
    ALL = "all"
    CLOSED = "closed"
    OPEN = "open"

    def __str__(self) -> str:
        return str(self.value)
