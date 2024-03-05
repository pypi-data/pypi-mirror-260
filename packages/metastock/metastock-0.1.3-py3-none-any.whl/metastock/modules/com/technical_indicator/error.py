from metastock.modules.core.util.app_error import AppError


class DateNotSetError(AppError):
    def __init__(self, message='Please set date before run get data', code='com_technical_indicator_000'):
        super().__init__(message, code)


class ConfigNotSetError(AppError):
    def __init__(self, message='Please set config before run get data', code='com_technical_indicator_000'):
        super().__init__(message, code)
