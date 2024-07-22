from app import app
from models import db, User

from unittest import TestCase

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:Kwok17273185@localhost:5432/blogly"
)
app.config["SQLALCHEMY_ECHO"] = False

# Start from scratch every time this test file runs
db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Testing User veiws"""

    def setUp(self):
        """Add sample pet."""

        User.query.delete()

        user = User(first_name="Jacky", last_name="Chan", image_url="url")

        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_pets(self):
        with app.test_client() as client:

            resp = client.get("/", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

    def test_users_list(self):

        # Make request to flask via `client`
        with app.test_client() as client:

            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Users</h1>", html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>User Detail Page</h1>", html)
            self.assertIn(self.user.first_name, html)

    def test_create_user(self):
        with app.test_client() as client:

            data = {"first-name": "Winton", "last-name": "Wong", "image-url": "url"}
            resp = client.post("/users/new", data=data)

            self.assertEqual(resp.status_code, 302)
