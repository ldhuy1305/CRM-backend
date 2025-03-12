from enum import Enum
FULL_DAY_FORMAT = "%Y-%m-%d %H:%M:%S"

DAY_FORMAT = "%Y%m%d"

DAY_EXCEL_FORMAT = "%Y/%m/%d"

class UserRoleEnum(Enum):
    ADMIN = 1
    SALES = 2
    MARKETING = 3

REGEX_CHECK_FORMAT_PASSWORD = (
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
)
