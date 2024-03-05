from enum import Enum


class MergePullRequestOptionDo(str, Enum):
    MANUALLY_MERGED = "manually-merged"
    MERGE = "merge"
    REBASE = "rebase"
    REBASE_MERGE = "rebase-merge"
    SQUASH = "squash"

    def __str__(self) -> str:
        return str(self.value)
