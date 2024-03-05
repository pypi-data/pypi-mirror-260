from metastock.modules.mbinance.error.fatal_error import FatalError


class ApiFailFatalError(FatalError):
    def __init__(
        self, message="Fatal Error from API", code="API_FAIL_FATAL_ERROR"
    ) -> None:
        super().__init__(message=message, code=code)
