from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate
import os

db = SQLAlchemy()
DB_NAME = "database.db"
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static', 'images')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', f'sqlite:///{DB_NAME}')
    app.config['SQLALCHEMY_BINDS'] = {
        'candidates': os.environ.get('CANDIDATES_DB_URL', 'sqlite:///Candidates.db'),
        'teachers': os.environ.get('TEACHERS_DB_URL', 'sqlite:///teachers.db')
    }
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    path = app.config['UPLOAD_FOLDER']
    if not os.path.exists(path):
        os.makedirs(path)

    db.init_app(app)
    migrate.init_app(app, db)
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




