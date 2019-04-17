import unittest
from app import app, db
from app.models import User
from app.app_forms import soft_block


class SoftBlockCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

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