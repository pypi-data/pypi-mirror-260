from marshmallow import EXCLUDE, Schema, fields, validate


class PriceHistorySchema(Schema):
    class Meta:
        unknown = EXCLUDE  # hoặc bạn có thể sử dụng INCLUDE

    date = fields.Date(required=True)
    high = fields.Integer(required=True, validate=validate.Range(min=0))
    low = fields.Integer(required=True, validate=validate.Range(min=0))
    close = fields.Integer(required=True, validate=validate.Range(min=0))
    open = fields.Integer(required=True, validate=validate.Range(min=0))
    volume = fields.Integer(required=True, validate=validate.Range(min=0))
    # totalTrade = fields.Integer(required=True, validate=validate.Range(min=0))
    # value = fields.Integer(required=True, validate=validate.Range(min=0))
    # buyCount = fields.Integer(required=True, validate=validate.Range(min=0))
    # buyQuantity = fields.Integer(required=True, validate=validate.Range(min=0))
    # sellCount = fields.Integer(required=True, validate=validate.Range(min=0))
    # sellQuantity = fields.Integer(required=True, validate=validate.Range(min=0))
    # Các trường mới
    fBuyVal = fields.Integer(validate=validate.Range(min=0))
    fBuyQty = fields.Integer(validate=validate.Range(min=0))
    fSellVal = fields.Integer(validate=validate.Range(min=0))
    fSellQty = fields.Integer(validate=validate.Range(min=0))


priceHistorySchema = PriceHistorySchema()
