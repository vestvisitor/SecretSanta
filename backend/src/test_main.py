from os import close
from traceback import print_tb

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, select
from sqlmodel.pool import StaticPool

from .main import app, hash_password
from .database import get_session
from .models import User

from faker import Faker

faker = Faker("ru_RU")


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite:///testing.db",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.mark.parametrize('execution_number', range(5))
def test_create_user(execution_number, client: TestClient):

    user_data = {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "password": faker.password(8)
    }

    response = client.post(
        "/user/",
        json=user_data
    )

    data = response.json()

    assert response.status_code == 200
    assert data["first_name"] == user_data["first_name"]
    assert data["last_name"] == user_data["last_name"]
    assert data["id"] is not None


# def test_create_user_incomplete(client: TestClient):
#
#     response = client.post(
#         "/user/",
#         json={
#             "fist_name": "Misha",
#             "password": "123l"
#         }
#     )
#
#     assert response.status_code == 422
#
#
# def test_create_user_invalid(client: TestClient):
#
#     response = client.post(
#         "/user/",
#         json={
#             "first_name": "Misha",
#             "last_name": "Cool",
#             "password": {"message": "there's no password"}
#         }
#     )
#
#     assert response.status_code == 422
#
#
# def test_read_users(session: Session, client: TestClient):
#     user = User(first_name="Misha", last_name="Goncharenko", hashed_password="secretlal")
#     session.add(user)
#     session.commit()
#     session.refresh(user)
#
#     response = client.get(f"/users/{user.id}")
#     data = response.json()
#
#     assert response.status_code == 200
#     assert data["first_name"] == user.first_name
#     assert data["last_name"] == user.last_name
#     assert data["id"] == f"{user.id}"
#
#
# def test_make_wish(session: Session, client: TestClient):
#     user = session.exec(select(User).where(User.last_name == "Goncharenko")).first()
#
#     response = client.post(
#         "/wish/",
#         json={
#             "name": "phone",
#             "link": "somerandomcite.com",
#             "priority": 5,
#             "creator_id": f"{user.id}"
#         }
#     )
#
#     data = response.json()
#
#     assert response.status_code == 200
#     assert data["name"] == "phone"
#     assert data["link"] == "somerandomcite.com"
#     assert data["priority"] == 5
