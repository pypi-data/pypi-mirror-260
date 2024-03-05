import math

import arrow
from flask_restx import Resource, reqparse, marshal_with
from werkzeug.exceptions import BadRequest

from metastock.flaskr.util.response import app_response_schema
from metastock.modules.com.technical_indicator.hullma import HullmaConfig, Hullma
from metastock.modules.com.util.avg import avg
from metastock.modules.core.util.app_error import AppError
from metastock.modules.core.util.pd.pd_to_datetime import pd_to_datetime
from metastock.modules.stockinfo.ulti.get_tick_history import get_tick_history
from metastock.modules.stockinfo.ulti.merge_tick_histories import merge_tick_histories
from metastock.modules.trade.analysis.hullma import StockTradingAnalysisHullma


class AnalysisHullmaIntraDay(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._create_parser()

    @marshal_with(app_response_schema)
    def get(self):
        args = self.parser.parse_args()
        symbol = args["symbol"]
        resolution = args["resolution"]
        from_date = args.get("from_date")
        to_date = args.get("to_date")

        tick_histories = get_tick_history(
            symbol,
            from_date=from_date or arrow.utcnow().shift(days=-1).format("YYYY-MM-DD"),
            to_date=to_date or arrow.utcnow().format("YYYY-MM-DD"),
        )
        grouped_ticks = []

        try:
            tick_data = merge_tick_histories(
                tick_histories=tick_histories, resolution=int(resolution)
            )

            hullma_config = HullmaConfig(
                length=16,
                cal_source_func=lambda row: avg(
                    row["close"], row["close"], row["open"], row["high"], row["low"]
                ),
            )
            hullma = Hullma(history=tick_data, symbol=symbol, skip_validate_price=True)
            hullma.set_config(hullma_config)
            hullma_data = hullma.get_data()

            hullma_analysis = StockTradingAnalysisHullma()
            hullma_analysis_data, _ = hullma_analysis.calculate_state_hullma(
                hullma_data
            )

            for grouped_tick in tick_data:
                pd_index = pd_to_datetime(grouped_tick["date"])
                hullma_trend_data = hullma_analysis_data.loc[pd_index]
                hullma_tick_data = hullma_data.loc[pd_index]
                grouped_ticks.append(
                    {
                        "hullma_trend": int(hullma_trend_data["trend"]),
                        "hullma": float(hullma_tick_data)
                        if not math.isnan(hullma_tick_data)
                        else "NaN",
                        **grouped_tick,
                    }
                )

        except AppError as e:
            raise BadRequest(e.message)

        return {
            "success": True,
            "data": {"grouped_ticks": grouped_ticks},
        }

    def _create_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "symbol",
            type=str,
            required=True,
            help="Symbol cannot be blank",
            location="args",
        )

        parser.add_argument(
            "resolution",
            type=str,
            required=True,
            help="resolution cannot be blank",
            location="args",
        )

        parser.add_argument(
            "from_date",
            type=str,
            required=False,
            location="args",
        )

        parser.add_argument(
            "to_date",
            type=str,
            required=False,
            location="args",
        )

        self.parser = parser
