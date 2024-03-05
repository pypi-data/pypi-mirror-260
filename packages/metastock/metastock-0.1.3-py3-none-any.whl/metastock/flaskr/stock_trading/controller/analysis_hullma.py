from flask import current_app
from flask_restx import marshal_with, reqparse, Resource

from metastock.flaskr.util.response import app_response_schema
from metastock.modules.com.technical_indicator.hullma import Hullma

# Khởi tạo parser
parser = reqparse.RequestParser()
parser.add_argument(
    "symbol", type=str, required=True, help="Symbol cannot be blank", location="args"
)


class AnalysisHullmaResource(Resource):
    @marshal_with(app_response_schema)
    def get(self):
        args = parser.parse_args()

        symbol = args["symbol"]

        current_app.logger.info(f"Process get Hullma for symbol '{symbol}'")

        hullma = Hullma(symbol=symbol)
        hullma_data = hullma.get_data()

        prices = hullma.get_price_helper().get_df()

        return {
            "success": True,
            "data": {
                "hull": [
                    {
                        "d": int(index.timestamp()),
                        "hull": hullma_data.get(index, None),
                        "c": float(value["close"]),
                        "o": float(value["open"]),
                        "h": float(value["high"]),
                        "l": float(value["low"]),
                    }
                    for index, value in prices.iterrows()
                ]
            },
        }
