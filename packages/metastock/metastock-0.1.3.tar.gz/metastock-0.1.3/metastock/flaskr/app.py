from flask import Flask, g, jsonify
from flask_cors import CORS

from metastock.flaskr.stock_trading import stock_trading
from metastock.modules.core.logging.logger import Logger

BLUEPRINTS = [stock_trading]


def create_app(app_name="metastock"):
    app = Flask(app_name)
    CORS(app)
    app.config.from_prefixed_env(prefix="FLASK")
    configure_logging(app)

    blueprints_fabrics(app, BLUEPRINTS)
    extensions_fabrics(app)

    error_pages(app)
    gvars(app)

    return app


def blueprints_fabrics(app, blueprints):
    """Configure blueprints in views."""

    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def extensions_fabrics(app):
    pass


def gvars(app):
    @app.before_request
    def gdebug():
        if app.debug:
            g.debug = True
        else:
            g.debug = False


def error_pages(app):
    # HTTP error pages definitions
    @app.errorhandler(403)
    def forbidden_page(error):
        return (
            jsonify(
                {
                    "error": "Forbidden",
                    "message": "You don't have permission to access this resource",
                }
            ),
            403,
        )

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({"error": "Not Found", "message": "Resource not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (
            jsonify(
                {
                    "error": "Method Not Allowed",
                    "message": "The method specified in the request is not allowed",
                }
            ),
            405,
        )

    @app.errorhandler(500)
    def server_error_page(error):
        return (
            jsonify(
                {
                    "error": "Internal Server Error",
                    "message": "An internal server error occurred",
                }
            ),
            500,
        )


def configure_logging(app):
    app._logger = Logger("flask_logger")
