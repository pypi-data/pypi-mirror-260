from metastock.modules.stockinfo.schema.tick_schema import tick_schema


class AnalysisTickConfig:
    def __init__(self, trade_value: int = 300, shark_collect_percent=60):
        self.shark_collect_percent = shark_collect_percent
        self.trade_value = trade_value


class StockTradingAnalysisTick:
    def __init__(self, tick_data, config: AnalysisTickConfig = AnalysisTickConfig()):
        self.config = config
        self.tick_data = tick_data
        tick_schema.load(tick_data)

    def get_data(self):
        meta = self.tick_data["meta"]
        tB, tS = self._cal_sum_buy_and_sell(tick_list=meta)

        valid_tick_by_trade_value = self._get_valid_tick_by_trade_value()
        ttB, ttS = self._cal_sum_buy_and_sell(tick_list=valid_tick_by_trade_value)

        buy_sell_info_at_price = self._cal_sum_buy_and_sell_price(
            tick_list=valid_tick_by_trade_value
        )

        is_shark_collect, shark_collect_from_price = self._check_if_shark_collect(
            tick_data=buy_sell_info_at_price
        )

        return {
            "trade_value": {
                "buy_total_buy_ratio": round(ttB * 100 / tB, 2)
                if tB > 0
                else 0,  # La buy thoa man trade value tren tong buy
                "sell_total_sell_ratio": round(ttS * 100 / tS)
                if tS > 0
                else 0,  # La sell thoa man trade value tren tong sell
                "buy_sell_ratio": round(ttB * 100 / (ttB + ttS))
                if ttB + ttS > 0
                else 0,
            },
            "buy_sell_ratio": round(tB * 100 / (tB + tS)) if tB + tS > 0 else 0,
            "is_shark_collect": is_shark_collect,
            "shark_collect_from_price": int(shark_collect_from_price)
            if shark_collect_from_price is not None
            else None,
        }

    def _check_if_shark_collect(self, tick_data: dict):
        sorted_keys = sorted(tick_data.keys(), reverse=True)
        tS = 0
        tB = 0

        lowest_price_picked = None

        for key in sorted_keys:
            tS += tick_data[key]["S"]
            tB += tick_data[key]["B"]

            if (
                tS + tB > 0
                and round(tB * 100 / (tS + tB), 2) > self.config.shark_collect_percent
            ):
                lowest_price_picked = int(key)

        return (
            (False, None)
            if lowest_price_picked is None
            else (True, lowest_price_picked)
        )

    def _get_valid_tick_by_trade_value(self):
        meta = self.tick_data["meta"]
        valid_ticks = []

        for t in meta:
            tick_value = t["vol"] * t["p"]
            if tick_value >= (self.config.trade_value * 10**6):
                valid_ticks.append(t)

        return valid_ticks

    def _cal_sum_buy_and_sell_price(self, tick_list: list):
        info = {}

        for t in tick_list:
            p = t["p"]

            if str(p) not in info:
                info[str(p)] = {"B": 0, "S": 0}

            if t["a"] == "B":
                info[str(p)]["B"] += p * t["vol"]

            if t["a"] == "S":
                info[str(p)]["S"] += p * t["vol"]

        return info

    def _cal_sum_buy_and_sell(self, tick_list: list):
        tB = 0
        tS = 0
        for t in tick_list:
            if t["a"] == "B":
                tB += t["vol"] * t["p"]

            if t["a"] == "S":
                tS += t["vol"] * t["p"]

        return tB, tS
