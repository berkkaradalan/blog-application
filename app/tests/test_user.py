from fastapi.testclient import TestClient
from main import app
import pytest
from app.config.helper import mongo_collections, get_password_hash, create_id, get_current_time

client = TestClient(app)

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    """
    Setup before each test and teardown after each test.
    For example, clear the database or reset the state.
    """
    mongo_collections.users.delete_many({"username": {"$regex": "testuser.*"}})
    yield

def test_register_success():
    """
    Test case for successful user registration.
    """
    generate_user = "testuser" + str(create_id())
    response = client.post(
        "/user/register",
        json={
            "username": generate_user,
            "name": "Test",
            "lastname": "User",
            "email": "testuser1@example.com",
            "password": "TestPassword123!",
            "password_confirm": "TestPassword123!",
        }
    )
    assert response.status_code == 200
    assert response.json()["message"] == "User created successfully!"

def test_register_username_taken():
    """
    Test case where the username is already taken.
    """
    generate_user = "testuser" + str(create_id())
    mongo_collections.users.insert_one({
        "username": generate_user,
        "name": generate_user,
        "lastname": generate_user,
        "email": f"{generate_user}@example.com",
        "password": get_password_hash(generate_user),
    })

    response = client.post(
        "/user/register",
        json={
            "username": generate_user,
            "name": generate_user,
            "lastname": generate_user,
            "email": f"{generate_user}@example.com",
            "password": generate_user,
            "password_confirm": generate_user,
        }
    )
    assert response.status_code == 409
    assert "This username is already taken, please choose another." in response.json()["detail"]


def test_register_invalid_email():
    """
    Test case where the provided email is invalid.
    """
    generate_user = "testuser" + str(create_id())
    response = client.post(
        "/user/register",
        json={
            "username": generate_user,
            "name": "Test",
            "lastname": "User",
            "email": "invalid-email",
            "password": "TestPassword123!",
            "password_confirm": "TestPassword123!",
        }
    )
    assert response.status_code == 400
    assert "Email is not valid." in response.json()["detail"]

def test_get_profile_detail_success():
    """
    Test case for get profile detail success case.
    """
    generate_user =  "testuser" + str(create_id())
    user_timestamp = get_current_time()
    mongo_collections.users.insert_one({
        "user_id":generate_user,
        "username": generate_user,
        "name": generate_user,
        "lastname": generate_user,
        "email": f"{generate_user}@mail.com",
        "password": get_password_hash("testuser83b38c8d-becf-4ce7-9686-a66798d5d300"),
        "user_created_at":user_timestamp,
        "user_updated_at":user_timestamp
    })

    response = client.get(
        "/user/get-profile-detail",
        params={"user_id":generate_user}
    )
    assert response.status_code == 200
    assert response.json() == {
        "user_id":generate_user,
        "username": generate_user,
        "name": generate_user,
        "lastname": generate_user,
        "email": f"{generate_user}@mail.com",
        "user_created_at":user_timestamp,
        "user_updated_at":user_timestamp
    }

def test_get_profile_detail_user_not_found():
    """
    Test case for get profile detail user not found case.
    """
    response = client.get(
        "/user/get-profile-detail",
        params={"user_id":str(create_id())}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found!."}