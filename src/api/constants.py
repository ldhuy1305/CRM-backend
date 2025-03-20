from enum import Enum

FULL_DAY_FORMAT = "%Y-%m-%d %H:%M:%S"

DAY_FORMAT = "%Y%m%d"

DAY_EXCEL_FORMAT = "%Y/%m/%d"

REGEX_CHECK_FORMAT_PASSWORD = (
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
)


class ActionEnum(Enum):
    ADD = "add"
    CHANGE = "change"
    DELETE = "delete"
    VIEW = "view"
    CONVERT = "convert"
    ASSIGN_TO_OTHER = "assign_to_other"
    CLOSE = "close"
    COMPLETE = "complete"


class ModuleEnum(Enum):
    LEAD = "lead"
    CONTACT = "contact"
    ACCOUNT = "account"
    DEAL = "deal"
    CAMPAIGN = "campaign"
    TASK = "task"
    MEETING = "meeting"
    CALL = "call"
    REPORT = "report"
    USER = "user"


class GroupNameEnum(Enum):
    ADMIN = "Admin"
    MANAGER = "Manager"
    SALESMAN = "Salesman"
    MARKETER = "Marketer"
