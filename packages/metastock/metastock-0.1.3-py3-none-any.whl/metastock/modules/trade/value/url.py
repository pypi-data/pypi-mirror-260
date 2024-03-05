from metastock.modules.core.util.app_error import AppError
from metastock.modules.core.util.environment import env


class TradeUrlValue:
    LIVE_BASE_URL = "https://stock.ngocdiep.top"

    @property
    def TRADING_STRATEGY_PROCESS_URL(self):
        return (
            env().get("API_END_POINT") + "/strategy/process"
            if env().get("API_END_POINT") is not None
            else None
        )

    def get_tick_intraday_speed_url(self, symbol: str, date: str) -> str:
        return (
            TradeUrlValue.LIVE_BASE_URL
            + f"/market-tick-action/intra-day-speed?symbol={symbol}&date={date}"
        )

    def get_stock_trading_analysis_url(self):
        return f"{TradeUrlValue.LIVE_BASE_URL}/stock-trading/analysis"

    def get_stock_trading_save_analysis_url(self):
        base_url = self._get_base_url()

        return f"{base_url}/stock-trading/analysis"

    def get_stock_trading_bulk_submit(self):
        base_url = self._get_base_url()

        return f"{base_url}/strategy/bulk-submit-action"

    def get_stock_trading_patch_process(self):
        base_url = self._get_base_url()

        return f"{base_url}/strategy/process"

    def get_strategy_processes(self, strategy_hash: str):
        base_url = self._get_base_url()

        return f"{base_url}/strategy/strategy-processes?hash={strategy_hash}"

    def get_strategy_process_actions(self, strategy_hash: str, symbol=str):
        base_url = self._get_base_url()

        return f"{base_url}/strategy/strategy-process-actions?hash={strategy_hash}&symbol={symbol}"

    def _get_base_url(self):
        if env().get("API_END_POINT") is None:
            raise AppError("Missing PS_API_END_POINT env config")

        return env().get("API_END_POINT")
