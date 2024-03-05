from enum import Enum


class RepoListPullRequestsSort(str, Enum):
    LEASTCOMMENT = "leastcomment"
    LEASTUPDATE = "leastupdate"
    MOSTCOMMENT = "mostcomment"
    OLDEST = "oldest"
    PRIORITY = "priority"
    RECENTUPDATE = "recentupdate"

    def __str__(self) -> str:
        return str(self.value)
