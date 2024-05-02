import pytest
from fastapi.testclient import TestClient
from ..app.main import app
from ..app.database import get_db, Base

from ..app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..app.oauth2 import create_access_token

from ..app.models import Post

# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:admin@localhost:5432/fastapi_test"
engine = create_engine(url=SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


@pytest.fixture(scope='function')
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope='function')
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {
        "email": "demo_user@gmail.com",
        "password": "password"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {
        "email": "demo_user2@gmail.com",
        "password": "password"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({'user_id': test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [
        {
            "title": "first title",
            "content": "first content",
            "owner_id": test_user['id']
        },
        {
            "title": "second title",
            "content": "second content",
            "owner_id": test_user['id']
        },
        {
            "title": "third title",
            "content": "third content",
            "owner_id": test_user['id']
        },
        {
            "title": "fourth title",
            "content": "fourth content",
            "owner_id": test_user2['id']
        }
    ]
    for post_data in posts_data:
        post = Post(**post_data)
        session.add(post)
    session.commit()
    
    posts = session.query(Post).all()
    return posts
    
    
