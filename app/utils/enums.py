import enum
from app.interfaces.runnerFactory import ExponeaRequestRunnerFactory


class TaskTypes(enum.Enum):
    ALL_SUCCESSFUL = 0
    FIRST_SUCCESSFUL = 1
    WITHIN_TIMEOUT = 2
    SMART = 3


class SourceTypes(enum.Enum):
    EXPONEA = ExponeaRequestRunnerFactory


class URLList(enum.Enum):
    EXPONEA_TEST_SERVER = (
        "https://exponea-engineering-assignment.appspot.com/api/work"
    )
