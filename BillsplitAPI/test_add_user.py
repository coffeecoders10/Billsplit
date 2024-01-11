import unittest
from flask import Flask
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
from app import app, db, User  # Replace "your_app" with the actual name of your Flask app module
from unittest.mock import patch, MagicMock

class TestAddUserRoute(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database for testing
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_user(self):
        # Test the 'add_user' route with valid data
        data = {'username': 'test_user', 'mail': 'test@example.com'}
        response = self.app.post('/add_user', data=data)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"User Added Successfully!", response.data)

        # Verify that the user was added to the database
        user = User.query.filter_by(user_username='test_user', user_mail='test@example.com').first()
        self.assertIsNotNone(user)

    def test_add_user_missing_data(self):
        # Test the 'add_user' route with missing data
        data = {'username': 'test_user'}  # 'mail' is missing
        response = self.app.post('/add_user', data=data)

        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Data not found", response.data)

        # Verify that no user was added to the database
        users_count = User.query.count()
        self.assertEqual(users_count, 0)

class TestGoogleOAuth(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SERVER_NAME'] = 'localhost.localdomain'
        self.app = app.test_client()

    def test_home_route_authenticated(self):
        with patch('app.google.authorized_response', return_value={'access_token': 'fake_access_token'}):
            with patch('app.google.get', return_value=MagicMock(data={'email': 'test@example.com', 'id': '123'})):
                with self.app.session_transaction() as session:
                    session['google_token'] = ('fake_access_token', '')
                response = self.app.get('/')
                self.assertIn(b'Logged in as: test@example.com<br>Google User ID: 123', response.data)

    def test_home_route_not_authenticated(self):
        response = self.app.get('/')
        self.assertIn(b'Not logged in', response.data)

    def test_login_route(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 302)  # Should redirect to Google login

    def test_logout_route(self):
        with self.app.session_transaction() as session:
            session['google_token'] = ('fake_access_token', '')
        response = self.app.get('/logout')
        self.assertEqual(response.status_code, 302)  # Should redirect to home

if __name__ == '__main__':
    unittest.main()
