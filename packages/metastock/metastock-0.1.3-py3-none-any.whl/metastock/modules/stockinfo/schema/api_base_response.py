from marshmallow import fields, EXCLUDE


class ApiBaseResponse:
    class Meta:
        unknown = EXCLUDE  # hoặc bạn có thể sử dụng INCLUDE

    success = fields.Boolean(required=True)
    message = fields.String(required=True)
    data = fields.Raw()
    error = fields.String(required=False)


api_base_response = ApiBaseResponse()
