from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from src.database.models import db
from flask import Flask, render_template


def index():
    return render_template('index.html')


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 3600
    app.config['SECRET_KEY'] = 'secret!'

    app.add_url_rule('/', 'index', index)

    from app import app_bp
    app.register_blueprint(app_bp, url_prefix='/api')

    from src.database.models import db
    db.init_app(app)

    return app


app = create_app('config.development')

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
