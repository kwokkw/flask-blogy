from unittest import TestCase
from app import app
from models import db, User

# Use test database
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:Kwok17273185@localhost:5432/blogly_test"
)
app.config["SQLALCHEMY_ECHO"] = False

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    def setUp(self):
        User.query.delete()

    def tearDown(self):
        db.session.rollback()

    def test_user(self):
        user = User(first_name="John", last_name="Doe", image_url="www.image.html")
        db.session.add(user)
        db.session.commit()

        test_user = User.query.get(user.id)
        count = User.query.count()

        self.assertEqual(test_user.first_name, "John")
        self.assertEqual(test_user.last_name, "Doe")
        self.assertEqual(test_user.image_url, "www.image.html")
        self.assertEqual(count, 1)
