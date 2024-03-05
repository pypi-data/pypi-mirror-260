from flask import current_app
from flask_restx import reqparse, Resource

from metastock.modules.trade.analysis.foreign import StockTradingAnalysisForeign

parser = reqparse.RequestParser()
parser.add_argument(
    "symbol", type=str, required=True, help="Symbol cannot be blank", location="args"
)


class AnalysisForeign(Resource):
    def get(self):
        args = parser.parse_args()

        symbol = args["symbol"]

        current_app.logger.info(f"Process get Foreign data for symbol '{symbol}'")

        foreign = StockTradingAnalysisForeign(symbol)

        return {"success": True, "data": []}
