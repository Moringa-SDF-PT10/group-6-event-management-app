import sys
import os
import pytest
import json


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.user import User
from app.config import TestConfig

# Pytest fixture
@pytest.fixture(scope='function')
def test_client():
    """Create and configure a new app instance for each test."""
    app = create_app(TestConfig)
    client = app.test_client()

    # Establish an application context before running the tests.
    with app.app_context():
        db.create_all()
        yield client
        db.session.remove()
        db.drop_all()

# Sample user data to be used across multiple tests
user_data = {
    "firstName": "Test",
    "lastName": "User",
    "phoneNumber": "1234567890",
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "role": "attendee"
}

# --- Test Functions ---

def test_successful_signup(test_client):
    """ ✅ GIVEN a user's details
        WHEN a POST request is made to /signup
        THEN check that the response is 201 and the user is in the database
    """
    res = test_client.post('/signup', data=json.dumps(user_data), content_type='application/json')
    assert res.status_code == 201
    response_data = res.get_json()
    assert 'access_token' in response_data
    assert 'user' in response_data
    
    user = User.query.filter_by(email=user_data['email']).first()
    assert user is not None

def test_signup_with_existing_email(test_client):
    """ ❌ GIVEN a user already exists
        WHEN a POST request is made to /signup with the same email
        THEN check that the response is 409
    """
    test_client.post('/signup', data=json.dumps(user_data), content_type='application/json')
    res = test_client.post('/signup', data=json.dumps(user_data), content_type='application/json')
    assert res.status_code == 409
    assert 'Username or email already exists' in res.get_json()['error']

def test_successful_login(test_client):
    """ ✅ GIVEN a registered user
        WHEN a POST request is made to /login with correct credentials
        THEN check that the response is 200 and an access token is returned
    """
    test_client.post('/signup', data=json.dumps(user_data), content_type='application/json')
    login_data = {"username": "testuser", "password": "password123"}
    res = test_client.post('/login', data=json.dumps(login_data), content_type='application/json')
    assert res.status_code == 200
    assert 'access_token' in res.get_json()

def test_login_with_wrong_password(test_client):
    """ ❌ GIVEN a registered user
        WHEN a POST request is made to /login with incorrect credentials
        THEN check that the response is 401
    """
    test_client.post('/signup', data=json.dumps(user_data), content_type='application/json')
    login_data = {"username": "testuser", "password": "wrongpassword"}
    res = test_client.post('/login', data=json.dumps(login_data), content_type='application/json')
    assert res.status_code == 401
    assert 'Invalid username or password' in res.get_json()['error']

def test_successful_logout(test_client):
    """ ✅ GIVEN a logged-in user with a valid token
        WHEN a POST request is made to /logout
        THEN check that the token is successfully revoked
    """
    test_client.post('/signup', data=json.dumps(user_data), content_type='application/json')
    login_res = test_client.post('/login', data=json.dumps({"username": "testuser", "password": "password123"}), content_type='application/json')
    token = login_res.get_json()['access_token']
    
    # Logout with the token
    logout_res = test_client.post('/logout', headers={'Authorization': f'Bearer {token}'})
    assert logout_res.status_code == 200
    assert 'Logout successful.' in logout_res.get_json()['message']

    # Try to access a protected route with the revoked token
    profile_res = test_client.get('/profile', headers={'Authorization': f'Bearer {token}'})
    assert profile_res.status_code == 401
    assert 'Token has been revoked' in profile_res.get_json()['msg']
