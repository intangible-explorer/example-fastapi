import pytest
from jose import JWTError, jwt
from ..app.serializers import RetrieveUserSerializer
from ..app.serializers import TokenSerializer
from ..app.config import settings


def test_root(client):
    response = client.get("/")
    assert response.json().get('message') == "hello world"
    assert response.status_code == 200

def test_create_user(client):
    response = client.post("/users/", json={"email": "test@gmail.com", "password": "password"})
    new_user = RetrieveUserSerializer(**response.json())
    assert new_user.email == "test@gmail.com"
    assert response.status_code == 201

def test_login_user(test_user, client):
    response = client.post("/auth/login", data={"username": test_user['email'], "password": test_user['password']})
    login_response = TokenSerializer(**response.json())

    payload = jwt.decode(login_response.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    user_id = payload.get('user_id')

    assert login_response.token_type == "bearer"
    assert user_id == test_user['id']

@pytest.mark.parametrize("email, password, status_code", [
    ('test@gmail', 'password', 400),
    ('demo_user@gmail.com', 'wrong_password', 401),
    ('test@gmail', 'wrong_password', 400),
    (None, 'wrong_password', 422),
    ('test@gmail', None, 422),
])
def test_incorrect_login(test_user, client, email, password, status_code):
    response = client.post("/auth/login", data={"username": email, "password": password})
    assert response.status_code == status_code