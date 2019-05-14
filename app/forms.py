from datetime import datetime
from flask_security.forms import LoginForm

from app.models import User
from app.utils import soft_block


class CustomLoginForm(LoginForm):
    def validate(self):

        # Put code here if you want to do stuff before login attempt
        response = super(CustomLoginForm, self).validate()
        # Put code here if you want to do stuff after login attempt
        user = User.query.filter_by(email=self.email.data).first()
        if user.unsuccessful_login_count is None:
            user.unsuccessful_login_count = 0
        if user.blocked_until is None:
            user.blocked_until = datetime.utcnow()
        locktime = (datetime.utcnow() - user.blocked_until).total_seconds()
        soft_block(user, locktime)

        return response
