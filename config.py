import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    # A secret key that will be used for securely signing the session
    # cookie and can be used for any other security related needs
    # by extensions or your application.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # a way to DB
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # flask-security configurations
    SECURITY_REGISTERABLE = os.environ.get('SECURITY_REGISTERABLE', True)
    SECURITY_SEND_REGISTER_EMAIL = os.environ.get('SECURITY_SEND_REGISTER_EMAIL', False)
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT')
    SECURITY_TRACKABLE = os.environ.get('SECURITY_TRACKABLE', True)

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = os.environ.get('ADMINS')

    # secure upload configurations
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')

    #google drive api configurations
    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = os.path.join(basedir, 'project_service_account_file.json')
    FOLDER_ID = os.environ.get('FOLDER_ID') # your google drive folder ID
    FILE_PATH = os.path.join(UPLOAD_FOLDER, '{}')

    # soft block configurations
    MAX_UNSUCCESSFUL_LOGIN_ATTEMPTS = int(os.environ.get('MAX_UNSUCCESSFUL_LOGIN_ATTEMPTS') or 5)
    LOCK_TIME = int(os.environ.get('LOCK_TIME') or 60)

    #Heroku settings
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
