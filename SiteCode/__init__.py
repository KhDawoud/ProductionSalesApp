from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from SiteCode.config import Config
from flask_login import LoginManager

db = SQLAlchemy()
csrf = CSRFProtect()
bcrypt = Bcrypt()
login = LoginManager()
login.login_view = 'sales.login'
login.login_message = ""


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    csrf.init_app(app)
    login.init_app(app)
    bcrypt.init_app(app)

    from SiteCode.Main.routes import main
    from SiteCode.Salesperson.routes import sales_person
    from SiteCode.Admin.routes import admin

    app.register_blueprint(main)
    app.register_blueprint(sales_person)
    app.register_blueprint(admin)

    return app

