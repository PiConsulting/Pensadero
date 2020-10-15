from marshmallow import fields
from flask_marshmallow import Marshmallow


ma = Marshmallow()


class RoleSchema(ma.Schema):
    id = fields.Integer()
    role_name = fields.String(required=True)


class UserSchema(ma.Schema):
    id = fields.Integer()
    role_id = fields.Integer(required=True)
    username = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)

