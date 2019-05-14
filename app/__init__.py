from flask import Flask
from flask_mail import Mail
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_security import Security, SQLAlchemyUserDatastore

from config import Config
from app.forms import CustomLoginForm


migrate = Migrate()
bootstrap = Bootstrap()
mail = Mail()
security = Security()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.models import db, User, Role
    from app.routes import main_page

    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    mail.init_app(app)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore, login_form=CustomLoginForm)

    app.register_blueprint(main_page)

    return app
