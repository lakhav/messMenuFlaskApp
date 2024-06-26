from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate


db = SQLAlchemy()
admin = Admin()
migrate = Migrate()


DB_NAME = "database.db"

from . models import User,Menu, MenuItem, Day, Hostel,Timetable,Department,Subgroup

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Hostel, db.session))
admin.add_view(ModelView(Timetable, db.session))
admin.add_view(ModelView(Department, db.session))
admin.add_view(ModelView(Subgroup, db.session))
admin.add_view(ModelView(Menu, db.session))
admin.add_view(ModelView(MenuItem, db.session))



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'qweasdfsdf'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    admin.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    migrate.init_app(app, db)

    

    from .models import User
    
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Created Database!')
