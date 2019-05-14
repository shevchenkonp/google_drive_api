import os

from datetime import datetime
from werkzeug.utils import secure_filename
from flask_security.utils import verify_password
from flask import request, flash, current_app as app

from app.models import db


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def secure_upload(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            try:
                os.makedirs(app.config['UPLOAD_FOLDER'])
            except PermissionError:
                print("Can`t create folder. Please try run app again as Administrator")
                return False
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return True
    else:
        flash('PROHIBITED FORMAT!')
        return False


def lock_time_is_out(locktime):
    if locktime >= app.config['LOCK_TIME']:
        return True
    else:
        return False


def unlock_user(user):
    user.blocked_until = None
    user.active = True
    user.unsuccessful_login_count = 0


def lock_user(user):
    user.active = False
    user.blocked_until = datetime.utcnow()


def soft_block(user, locktime):
    if user.is_active:
        if not verify_password(request.form['password'], user.password) and \
                user.unsuccessful_login_count < app.config['MAX_UNSUCCESSFUL_LOGIN_ATTEMPTS']:
            user.unsuccessful_login_count = user.unsuccessful_login_count + 1

            if user.unsuccessful_login_count >= app.config['MAX_UNSUCCESSFUL_LOGIN_ATTEMPTS']:
                lock_user(user)
    else:
        if lock_time_is_out(locktime):
            unlock_user(user)
        else:
            flash('Your account is locked for {} seconds'.format(int(app.config['LOCK_TIME'] - locktime)))

    db.session.add(user)
    db.session.commit()
