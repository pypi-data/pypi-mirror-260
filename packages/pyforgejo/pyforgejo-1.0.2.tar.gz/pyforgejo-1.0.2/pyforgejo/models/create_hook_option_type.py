from enum import Enum


class CreateHookOptionType(str, Enum):
    DINGTALK = "dingtalk"
    DISCORD = "discord"
    FEISHU = "feishu"
    FORGEJO = "forgejo"
    GITEA = "gitea"
    GOGS = "gogs"
    MSTEAMS = "msteams"
    PACKAGIST = "packagist"
    SLACK = "slack"
    TELEGRAM = "telegram"
    WECHATWORK = "wechatwork"

    def __str__(self) -> str:
        return str(self.value)
