from flask_restx import Api


class BaseRestApi:
    INSTANCE: Api = None

    def register_blueprint(self, blueprint, **kwargs):
        BaseRestApi.INSTANCE = Api(blueprint, **kwargs)

        return self

    def get_api(self):
        return BaseRestApi.INSTANCE
