import pytest
from datetime import datetime, timedelta
import jwt
from apps import create_app


def create_auth_token():
    secret_key = b'9Jx#\xdd\x0f1\xf4\xa6\x8f\t\x97\x14\x1dh\xe6'

    token = jwt.encode({
        'sub': 'hola@gmail.com',
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(hours=3)},
        secret_key)

    return token


@pytest.fixture(scope='session')
def test_client():
    app, mongo = create_app('config.TestConfig')

    # Create a test client using the Flask application configured for testing
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            yield testing_client, mongo  # this is where the testing happens!
