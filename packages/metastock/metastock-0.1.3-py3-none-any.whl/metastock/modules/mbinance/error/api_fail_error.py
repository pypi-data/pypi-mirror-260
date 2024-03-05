from metastock.modules.mbinance.error.mbinance_error import MBinanceError


class ApiFailError(MBinanceError):
    def __init__(self, message="Error from API", code="API_FAIL_ERROR") -> None:
        super().__init__(message=message, code=code)
