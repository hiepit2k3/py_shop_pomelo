from marshmallow import Schema, fields

class Tokenschema(Schema):
    refresh_token = fields.Str(required=True)
    access_token = fields.Str(required=True)