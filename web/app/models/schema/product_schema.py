from marshmallow import Schema, fields

class ProductSchema(Schema):
    id = fields.Integer()
    name = fields.Str(required=True)
    price = fields.Str(required=True)
    quantity = fields.Str(required=True)
    image = fields.Str(required=True)
    
