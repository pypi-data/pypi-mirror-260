from flask import Blueprint
from werkzeug.exceptions import HTTPException

from metastock.flaskr.stock_trading.api import StockTradingApi
from metastock.flaskr.stock_trading.controller.analysis_foreign import AnalysisForeign
from metastock.flaskr.stock_trading.controller.analysis_hullma import (
    AnalysisHullmaResource,
)
from metastock.flaskr.stock_trading.controller.analysis_hullma_intra_day import (
    AnalysisHullmaIntraDay,
)

stock_trading = Blueprint("stock_trading", __name__, url_prefix="/stock-trading")

api = StockTradingApi().register_blueprint(blueprint=stock_trading).get_api()


@api.errorhandler(HTTPException)
def handle_exception(e):
    return (
        {"success": False, "error": e.name, "message": e.description},
        e.code,
    )


# Controller
api.add_resource(AnalysisHullmaResource, "/analysis/hullma")
api.add_resource(AnalysisForeign, "/analysis/foreign")
api.add_resource(AnalysisHullmaIntraDay, "/analysis/hullma-intra-day")
