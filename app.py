from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

def create_app():
    app = Flask(__name__ , template_folder = 'templates' , static_folder='static' , static_url_path='/')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./maindatabase.db'

    app.secret_key = 'SAMPLE KEY'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)


    from models import Users , Tasks

    @login_manager.user_loader
    def load_user(uid):
        return Users.query.get(uid)

    bcrypt = Bcrypt(app)
    
    from routes import register_routes
    register_routes(app, db, bcrypt)

    migrate = Migrate(app ,db)

    return app
