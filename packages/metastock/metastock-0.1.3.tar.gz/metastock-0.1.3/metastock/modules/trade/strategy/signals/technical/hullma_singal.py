from metastock.modules.com.technical_indicator.hullma import Hullma, HullmaConfig
from metastock.modules.core.logging.logger import Logger
from metastock.modules.core.util.pd.pd_to_datetime import pd_to_datetime
from metastock.modules.trade.strategy.signals.output_schema import SIGNAL_OUTPUT_SCHEMA_V1_NAME
from metastock.modules.trade.strategy.signals.signal_abstract import SignalAbstract
from metastock.modules.trade.util.predict_trend_change import predict_trend_change_v1


class HullmaSignal(SignalAbstract):
    name = 'hullma_signal'

    def support_output_versions(self) -> list[str]:
        return [SIGNAL_OUTPUT_SCHEMA_V1_NAME]

    def get_output(self, version=SIGNAL_OUTPUT_SCHEMA_V1_NAME):
        if version == SIGNAL_OUTPUT_SCHEMA_V1_NAME:
            return self._get_output_v1()

    def _get_output_v1(self):
        Logger().info("Will generate Hullma output v1 ")
        price_history = self.get_strategy().get_price_history()
        input_data = self.get_input()

        hullma_input: dict = input_data.get('hullma')
        hullma_config = HullmaConfig()
        if hullma_input is not None:
            hullma_length = hullma_input.get('length')

            if hullma_length is not None:
                hullma_config.length = hullma_length

        symbol = self.get_strategy().get_symbol()
        hullma = Hullma(symbol=symbol, history=price_history)
        hullma.set_config(hullma_config)
        hullma_data = hullma.get_data()

        Logger().ok(f"generated Hullma data for {symbol}")

        # just only for alerting
        Logger().info(f"Will generate predict_trend_change_v1 for {symbol}")
        predict_trend = predict_trend_change_v1(hullma_data)
        Logger().ok(f"generated predict_trend_change_v1 for {symbol}")

        Logger().info(f"Will build Hullma output for {symbol}")
        results = []
        for price in price_history:
            date = price['date']

            desired_date = pd_to_datetime(date)
            day_signal = {
                "date" : date,
                "buy"  : {},
                "sell" : {},
                "alert": {
                    "notify": False
                }
            }

            try:
                predict_trend_day = predict_trend.loc[desired_date, "next_day"]
                predict_trend_current_day = predict_trend.loc[desired_date, "estimate_day_change"]
                predict_trend_type = predict_trend.loc[desired_date, "trend"]

                if predict_trend_day:
                    day_signal["alert"] = {
                        "notify" : True,
                        "message": f"{symbol}: Detect hullma change next day {date} with trend {predict_trend_type} config length {hullma_config.length}"
                    }
                elif predict_trend_current_day == 0:
                    day_signal["alert"] = {
                        "notify" : True,
                        "message": f"{symbol}: Detect hullma change current day {date} with trend {predict_trend_type} config length {hullma_config.length}"
                    }
            except Exception as e:
                # Logger().warning(
                #     "An error occurred when get predict trend for date {desired_date}: %s", e,
                #     exc_info=False
                #     )
                pass

            results.append(day_signal)

        Logger().ok(f"built Hullma output for {self.strategy.get_symbol()}")
        return results
