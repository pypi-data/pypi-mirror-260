from marshmallow import fields, Schema

SIGNAL_OUTPUT_SCHEMA_V1_NAME = "@signal/output/v1"


class SignalOutputV1(Schema):
    pass


class SignalOutputV2(Schema):
    pass


class FixedBuyDateSchema(Schema):
    date = fields.Date()
    p = fields.Float()


class FixedBuySchema(Schema):
    buy = fields.List(fields.Nested(FixedBuyDateSchema))
