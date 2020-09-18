from flask_marshmallow import Schema
from marshmallow import fields
from marshmallow.validate import Length, Range


class TrackSchema(Schema):
    origin = fields.Str(require=True, validate=Length(max=3, min=3))
    destination = fields.Str(require=True, validate=Length(max=3, min=3))
    cost = fields.Float(validate=[Range(min=0)])
