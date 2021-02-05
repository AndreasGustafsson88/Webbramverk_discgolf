import unittest
import flask_unittest
from App.Data.Models.users import User
from App.UI import create_app


class TestRegistration(flask_unittest.ClientTestCase):
    app = create_app()
    app.config['WTF_CSRF_ENABLED'] = False

    def setUp(self, client) -> None:
        pass

    @staticmethod
    def assert_flashes(client, expected_message, expected_category='message'):
        with client.session_transaction() as session:
            try:
                category, message = session['_flashes'][0]
            except KeyError:
                raise AssertionError('nothing flashed')
            assert expected_message in message
            assert expected_category == category

    @staticmethod
    def create_user():
        return {
            "full_name": "test testsson",
            "user_name": "wack_a_tree",
            "email": "please_be_unique@mail.com",
            "password": "secret",
            "confirm_password": "secret"}

    def test_signup(self, client):
        user = self.create_user()
        response = client.post('/signup', data=user)
        self.assertStatus(response, 302)
        self.assertLocationHeader(response, 'http://localhost/')
        self.assertEqual(user['user_name'], User.find(user_name=user['user_name']).first_or_none().user_name)

    def test_signup_not_same_password(self, client):
        user = self.create_user()
        user['password'] = '123'
        client.post('/signup', data=user)
        self.assert_flashes(client, 'password are not the same')

    def test_email_already_exists(self, client):
        user = self.create_user()
        user['email'] = 'destroyer@discgolf.com'
        client.post('/signup', data=user)
        self.assert_flashes(client, 'Email already exists')

    def test_username_already_exists(self, client):
        user = self.create_user()
        user['user_name'] = 'Mcbeast'
        client.post('/signup', data=user)
        self.assert_flashes(client, 'Username already exists')

    def tearDown(self, client) -> None:
        user = self.create_user()
        User.delete_one(user_name=user['user_name'])


if __name__ == '__main__':
    unittest.main()
