from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    fullname = fields.Str(required=True)
    gender = fields.Str(required=True)
    country = fields.Str(required=True)
