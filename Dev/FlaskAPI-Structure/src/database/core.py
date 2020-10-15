from .models import RoleModel, UserModel


def get_role_by_id(role_id):
    return RoleModel.query.filter_by(id=role_id).first()


def get_role_by_name(role_name):
    return RoleModel.query.filter_by(role_name=role_name).first()


def create_role(role_schema):
    role = RoleModel(**role_schema)
    error = role.save()
    if not error:
        return role.id
    return error


def get_user_by_id(user_id):
    return UserModel.query.filter_by(id=user_id).first()


def get_user_by_username(username):
    return UserModel.query.filter_by(username=username).first()


def get_user_by_email(email):
    return UserModel.query.filter_by(email=email).first()


def get_all_user():
    return UserModel.query.all()


def create_user(user_schema):
    user = UserModel(**user_schema)
    error = user.save()
    if not error:
        return user.id
    return error


def update_user(user_id, user_schema):
    user = get_user_by_id(user_id)
    if user is not None:
        for attr in user_schema.keys():
            value = user_schema[attr]
            setattr(user, attr, value)

        error = user.save
        if not error:
            return user.id
        return error
    return {'error': 'User don\'t exists'}


def delete_user(user_id):
    user = UserModel.query.filter_by(id=user_id).first()
    user = user.remove()
    return user
