import unittest

from flask import current_app as app

from config import Config
from app import create_app
from app.models import User, db
from app.forms import soft_block


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class SoftBlockCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_lock_user(self):
        u = User(email='testmail@example.com', unsuccessful_login_count=app.config['MAX_UNSUCCESSFUL_LOGIN_ATTEMPTS'])
        db.session.add(u)
        db.session.commit()
        self.assertFalse(u.is_active)

    def test_unlock_user(self):
        u = User(email='testmail@example.com', active=False)
        locktime = app.config['LOCK_TIME']
        soft_block(u, locktime)
        db.session.add(u)
        db.session.commit()
        self.assertTrue(u.is_active)


if __name__ == '__main__':
    unittest.main()
