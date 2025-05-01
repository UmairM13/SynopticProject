import pytest
from fastapi.testclient import TestClient
from recommendation_engine.api.main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def test_client():
    return client

@pytest.fixture(scope="module")
def auth_header(test_client):
    # Login as a real user from your dummy data (u1@gmail.com, password)
    login_payload = {
        "email": "testuser@example.com",
        "password": "password123"
    }
    response = test_client.post("/travel/api/users/login", json=login_payload)
    assert response.status_code == 200
    data = response.json()
    session_token = data["session_token"]
    return {"X-Authorization": session_token}

def test_get_saved_recommendations(test_client, auth_header):
    response = test_client.get("/travel/api/recommendations/saved", headers=auth_header)
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, list)
        if data:
            assert "destination_id" in data[0]
            assert "destination" in data[0]
            assert "explanation" in data[0]
            assert "timestamp" in data[0]

def test_get_recommendations_for_user(test_client):
    response = test_client.get("/travel/api/recommendations/1")
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, list)
        if data:
            assert "id" in data[0]
            assert "name" in data[0]

def test_explain_destination(test_client):
    response = test_client.get("/travel/api/recommendations/explanation/1/1")
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        data = response.json()
        assert "destination" in data
        assert "explanation" in data

def test_preprocess_data(test_client):
    response = test_client.post("/travel/api/recommendations/preprocess")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)

def test_save_and_delete_recommendation(test_client, auth_header):
    save_payload = {
        "destination_id": 1,
        "destination_name": "Bali",
        "explanation": "Test explanation"
    }
    save_response = test_client.post("/travel/api/recommendations/save", json=save_payload, headers=auth_header)
    assert save_response.status_code == 200
    save_data = save_response.json()
    assert save_data["message"] == "Recommendation saved successfully"

    delete_response = test_client.delete("/travel/api/recommendations/save/1", headers=auth_header)
    assert delete_response.status_code == 200
    delete_data = delete_response.json()
    assert delete_data["message"] == "Recommendation deleted successfully"
