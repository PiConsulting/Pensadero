from flask import request
from flask_restful import Resource
from flask_cors import cross_origin
from database.schemas import RoleSchema, UserSchema
from database.core import (
    get_role_by_name,
    create_role,
    create_user,
    get_all_user
)



class UserView(Resource):
    """
    this is an example view and allow list all routes registered in this API (or routes.py file)
    """
    def __init__(self):
        super(UserView, self).__init__()
        self.role_schema = RoleSchema(unknown='EXCLUDE')
        self.user_schema = UserSchema(unknown='EXCLUDE')

    @cross_origin()
    def get(self):
        users = get_all_user()
        return {'users': users}, 200

    @cross_origin()
    def post(self):
        if request.is_json:
            data = request.get_json(force=True)
            role = get_role_by_name(data.get('role_name', 0))
            if not role:
                role_schema = self.role_schema.load(**data)
                result = create_role(role_schema)

            if isinstance(result, int):
                data.update({'role_id': result})
                user_schema = self.user_schema.load(**data)
                result = create_user(user_schema)
                if isinstance(result, int):
                    return {'new_user': result.id}, 200
        return result, 400
