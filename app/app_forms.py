from flask import request, flash
from flask_security.forms import LoginForm
from flask_security.utils import verify_password
from app import app, db
from app.models import User
from datetime import datetime


def lock_time_is_out(locktime):
    if locktime >= app.config['LOCK_TIME']:
        return True
    else:
        return False


def soft_block(user, locktime):
    if user.is_active:
        if not verify_password(request.form['password'], user.password) \
                and user.unsuccessful_login_count < \
                app.config['MAX_UNSUCCESSFUL_LOGIN_ATTEMPTS']:
            user.unsuccessful_login_count = user.unsuccessful_login_count + 1 if user.unsuccessful_login_count else 1

            if user.unsuccessful_login_count >= app.config['MAX_UNSUCCESSFUL_LOGIN_ATTEMPTS']:
                user.active = False
                user.blocked_until = datetime.utcnow()
    else:
        if lock_time_is_out(locktime):
            user.blocked_until = None
            user.active = True
            user.unsuccessful_login_count = 0
        else:
            flash('Your account is locked for {} seconds'.format(int(app.config['LOCK_TIME'] - locktime)))

    db.session.add(user)
    db.session.commit()


class CustomLoginForm(LoginForm):
    def validate(self):

        # Put code here if you want to do stuff before login attempt
        response = super(CustomLoginForm, self).validate()
        # Put code here if you want to do stuff after login attempt

        user = User.query.filter_by(email=self.email.data).first()
        locktime = (datetime.utcnow() - user.blocked_until).total_seconds()

        soft_block(user, locktime)

        return response
