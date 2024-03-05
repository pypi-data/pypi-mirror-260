from enum import Enum


class RepoListStatusesSort(str, Enum):
    HIGHESTINDEX = "highestindex"
    LEASTINDEX = "leastindex"
    LEASTUPDATE = "leastupdate"
    OLDEST = "oldest"
    RECENTUPDATE = "recentupdate"

    def __str__(self) -> str:
        return str(self.value)
