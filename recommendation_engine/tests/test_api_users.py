import pytest

# ---------------------- Create User ----------------------

def test_create_user_success(client):
    payload = {
        "email": "testuser@example.com",
        "password": "password123"
    }
    response = client.post("/travel/api/users/", json=payload)
    assert response.status_code == 200
    json_data = response.json()
    assert "id" in json_data
    assert json_data["email"] == "testuser@example.com"

# ---------------------- Login User ----------------------

def test_login_success(client):
    payload = {
        "email": "testuser@example.com",
        "password": "password123"
    }
    response = client.post("/travel/api/users/login", json=payload)
    assert response.status_code == 200
    json_data = response.json()
    assert "session_token" in json_data
    client.headers.update({"X-Authorization": json_data["session_token"]})

def test_login_failure_wrong_password(client):
    payload = {
        "email": "testuser@example.com",
        "password": "wrongpassword"
    }
    response = client.post("/travel/api/users/login", json=payload)
    assert response.status_code == 401

# ---------------------- Get Current User ----------------------

def test_get_current_user_success(client):
    response = client.get("/travel/api/users/me")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["email"] == "testuser@example.com"

def test_get_current_user_unauthenticated():
    from fastapi.testclient import TestClient
    from recommendation_engine.api.main import app

    unauth_client = TestClient(app)
    response = unauth_client.get("/travel/api/users/me")
    assert response.status_code == 401

# ---------------------- Update User ----------------------

def test_update_user_budget(client):
    user_id = int(client.get("/travel/api/users/me").json()["id"])
    payload = {
        "budget": 5000
    }
    response = client.patch(f"/travel/api/users/{user_id}", json=payload)
    assert response.status_code == 200
    updated = response.json()
    assert updated["budget"] == 5000

# ---------------------- Past Destinations ----------------------

def test_add_past_destination(client):
    user_id = int(client.get("/travel/api/users/me").json()["id"])
    payload = {
        "destination_name": "Paris",
        "trip_end_date": "2023-08-15"
    }
    response = client.post(f"/travel/api/users/{user_id}/past-destinations", json=payload)
    assert response.status_code == 200

def test_get_past_destinations(client):
    user_id = int(client.get("/travel/api/users/me").json()["id"])
    response = client.get(f"/travel/api/users/{user_id}/past-destinations")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# ---------------------- Logout User ----------------------

def test_logout(client):
    response = client.post("/travel/api/users/logout")
    assert response.status_code == 200

# ---------------------- Delete User ----------------------

def test_delete_user(client):
    response = client.delete("/travel/api/users/")
    assert response.status_code == 200
