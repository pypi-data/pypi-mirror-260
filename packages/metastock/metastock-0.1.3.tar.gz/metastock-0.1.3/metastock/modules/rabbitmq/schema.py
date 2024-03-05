from marshmallow import fields, Schema


class BodySchema(Schema):
    job_id = fields.String(required = True)
    payload = fields.Dict(required = True)


job_consumer_body_schema = BodySchema()
