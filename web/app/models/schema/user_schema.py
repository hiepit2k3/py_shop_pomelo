from marshmallow import Schema, fields

class UserSchema(Schema):
    username = fields.Str(required=True)
    fullname = fields.Str(required=True)
    gender = fields.Str(required=True)
    is_active = fields.Str(required=True)
    
