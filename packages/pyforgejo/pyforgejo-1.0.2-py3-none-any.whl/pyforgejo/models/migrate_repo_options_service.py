from enum import Enum


class MigrateRepoOptionsService(str, Enum):
    CODEBASE = "codebase"
    GIT = "git"
    GITBUCKET = "gitbucket"
    GITEA = "gitea"
    GITHUB = "github"
    GITLAB = "gitlab"
    GOGS = "gogs"
    ONEDEV = "onedev"

    def __str__(self) -> str:
        return str(self.value)
