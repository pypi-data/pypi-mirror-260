from enum import Enum


class IssueListIssuesState(str, Enum):
    ALL = "all"
    CLOSED = "closed"
    OPEN = "open"

    def __str__(self) -> str:
        return str(self.value)
