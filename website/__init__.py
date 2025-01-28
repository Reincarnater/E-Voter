from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"




def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = '/static/images/'
    app.config['SECRET_KEY'] = 'Please give us a passing grade :)'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_BINDS'] = {'candidates' : 'sqlite:///Candidates.db', 
                                      'teachers' : 'sqlite:///teachers.db'}
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    path = r"/static/images/"
    assert os.path.isfile(path)
    with open(path, "r") as f:
        pass
    

    db.init_app(app)
    app.app_context().push()

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Candidate
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
    



