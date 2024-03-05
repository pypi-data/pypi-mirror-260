from flask_restx import fields

app_response_schema = {
    "success": fields.Boolean,
    "data": fields.Raw(default={}),
}
