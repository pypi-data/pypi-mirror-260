from enum import Enum


class EditOrgOptionVisibility(str, Enum):
    LIMITED = "limited"
    PRIVATE = "private"
    PUBLIC = "public"

    def __str__(self) -> str:
        return str(self.value)
