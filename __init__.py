from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@localhost/MyDB'
    app.config['MAIL_SERVER']= "smtp.mailtrap.io"
    app.config['MAIL_USERNAME']='1639088e862249'
    app.config['MAIL_PASSWORD']='e76538fd0e5428'
    app.config['MAIL_PORT']='2525'
    app.config['UPLOAD_FOLDER']='C:\\Users\\Kareem\\Desktop\\task'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 * 1024
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'main.index'
    login_manager.init_app(app)
    mail.init_app(app)

    # blueprint for auth routes in our app
    # from .auth import auth as auth_blueprint
    # app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

