from metastock.modules.core.util.app_error import AppError


class CouldNotGetPriceHistory(AppError):
    def __init__(self, message="Could not get price history", code='stock_info_error_000'):
        super().__init__(message, code)


class CouldNotGetSymbolInfo(AppError):
    def __init__(self, message="Could not get symbol info", code='stock_info_error_000'):
        super().__init__(message, code)
