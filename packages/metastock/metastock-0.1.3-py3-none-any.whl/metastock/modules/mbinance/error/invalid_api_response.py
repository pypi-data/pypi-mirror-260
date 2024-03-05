from metastock.modules.mbinance.error.fatal_error import FatalError


class InvalidApiResponse(FatalError):
    def __init__(self, message, code="INVALID_API_RESPONSE"):
        super().__init__(message=message, code=code)
