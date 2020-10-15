from sqlalchemy import exc
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class ModelBase:

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            db.session.refresh(self)
        except exc.IntegrityError as ex:
            return {'error': f'Confict in Database: {ex.args[0].split(".")[4]}'}, 409
        except Exception as ex:
            return {'error': f'Data base error\n{ex}'}, 500

    def remove(self):
        try:
            db.session.delete(self)
            db.session.commit()
            db.session.refresh(self)
            return self
        except:
            return False


class RoleModel(ModelBase, db.Model):
    __tablename__ = 'roles'

    PERMISION = {'Admin': 1,
                 'Guest': 2,
                 'Unauthoried': 3
                 }

    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    role_name = db.Column('role_name', db.String(25), default='Unauthorized')

    def __init__(self, role_name):
        if role_name in self.PERMISION.keys():
            self.role_name = role_name

    def __repr__(self):
        return f'{self.role_name} role'


class UserModel(ModelBase, db.Model):
    __tablename__ = 'users'

    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    role_id = db.Column('role_id', db.ForeignKey('role.id', ondelete='CASCADE'), nullable=True)
    username = db.Column('username', db.String(255), unique=True)
    email = db.Column('email', db.String(255), unique=True)
    password = db.Column('password', db.String(255), nullable=False)
    last_update = db.Column('last_update', db.DateTime, server_default=db.func.current_timestamp(), nullable=True)

    def __init__(self, **kwargs):
        for key in kwargs:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

    def __repr__(self):
        return f'user {self.id}'
