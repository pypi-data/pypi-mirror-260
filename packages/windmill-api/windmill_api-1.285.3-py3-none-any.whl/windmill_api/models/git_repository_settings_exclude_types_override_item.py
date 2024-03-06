from enum import Enum


class GitRepositorySettingsExcludeTypesOverrideItem(str, Enum):
    APP = "app"
    FLOW = "flow"
    FOLDER = "folder"
    RESOURCE = "resource"
    RESOURCETYPE = "resourcetype"
    SCHEDULE = "schedule"
    SCRIPT = "script"
    SECRET = "secret"
    VARIABLE = "variable"

    def __str__(self) -> str:
        return str(self.value)
