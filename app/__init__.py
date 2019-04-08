from flask import Flask
from flask_mail import Mail
from google.oauth2 import service_account

from config import Config
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from googleapiclient.discovery import build


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)
mail = Mail(app)


credentials = service_account.Credentials.from_service_account_file(
    app.config['SERVICE_ACCOUNT_FILE'], scopes=app.config['SCOPES'])
service = build('drive', 'v3', credentials=credentials)


from app import routes, models
