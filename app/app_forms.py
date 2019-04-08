from flask import request, flash
from flask_security.forms import LoginForm
from flask_security.utils import verify_password
from app import app, db
from app.models import User
from datetime import datetime


class CustomLoginForm(LoginForm):
    def validate(self):

        # Put code here if you want to do stuff before login attempt
        response = super(CustomLoginForm, self).validate()
        # Put code here if you want to do stuff after login attempt

        user = User.query.filter_by(email=self.email.data).first()
        if user.blocked_until and ((datetime.utcnow() - user.blocked_until).total_seconds() > app.config['LOCK_TIME']):
            user.active = True

        if not verify_password(request.form['password'], user.password) and \
                user.unsuccessful_login_count < app.config['MAX_UNSUCCESSFUL_LOGIN_ATTEMPTS']:
            user.unsuccessful_login_count = user.unsuccessful_login_count + 1 if user.unsuccessful_login_count else 1
        elif user.unsuccessful_login_count == app.config['MAX_UNSUCCESSFUL_LOGIN_ATTEMPTS']:
            user.active = False
            user.blocked_until = datetime.utcnow()
            user.unsuccessful_login_count = 0
        elif not user.active:
            flash('Your account is locked for {} seconds'.format(
                (datetime.utcnow() - user.blocked_until).total_seconds()))
        db.session.add(user)
        db.session.commit()
        return response
