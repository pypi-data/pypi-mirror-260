from metastock.modules.core.util.app_error import AppError


class TradeFileNotFoundError(AppError):
    def __init__(self, message='Please check your config', code='trade_general_error_000'):
        super().__init__(message, code)


class StrategyNotFound(AppError):
    def __init__(self, message='Please check your strategy config', code='trade_general_error_000'):
        super().__init__(message, code)


class StrategySignalNotFound(AppError):
    def __init__(self, message='Please check your signal class name config', code='trade_general_error_000'):
        super().__init__(message, code)


class StrategyActionNotFound(AppError):
    def __init__(self, message='Please check your action class name config', code='trade_general_error_000'):
        super().__init__(message, code)


class StrategyFilterNotFound(AppError):
    def __init__(self, message='Please check your filter class name config', code='trade_general_error_000'):
        super().__init__(message, code)


class NotSupportConfigType(AppError):
    def __init__(self, message='Please check your config', code='trade_general_error_000'):
        super().__init__(message, code)


class UnknownMessageFromQueue(AppError):
    def __init__(self, message='Got unknown message from queue', code='trade_general_error_000'):
        super().__init__(message, code)


class ActionAndSignalNotMatch(AppError):
    def __init__(self, message="Action and signal's output not match ", code='trade_general_error_000'):
        super().__init__(message, code)


class CouldNotExecuteStrategy(AppError):
    def __init__(self, message="Could not execute strategy", code='trade_strategy_error_000'):
        super().__init__(message, code)


class CouldNotResolveUrlConfig(AppError):
    def __init__(self, message="Could not resolve url from env config", code='trade_strategy_error_000'):
        super().__init__(message, code)


class JobConsumerPayloadDataError(AppError):
    def __init__(self, message="missing or wrong payload data", code='trade_strategy_error_000'):
        super().__init__(message, code)


class StockTradingAnalysisNotFound(AppError):
    def __init__(self, message="Stock trading analysis not yet initialized", code='trade_strategy_error_000'):
        super().__init__(message, code)
