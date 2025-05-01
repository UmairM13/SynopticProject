import pytest
from fastapi.testclient import TestClient
from recommendation_engine.api.main import app

client = TestClient(app)


@pytest.fixture(scope="module")
def test_client():
    return client


def test_get_all_destinations_success(test_client):
    response = test_client.get("travel/api/destinations/")
    assert response.status_code == 200
    data = response.json()
    assert "destinations" in data
    assert isinstance(data["destinations"], list)
    if data["destinations"]:
        # Check expected fields on the first item
        first = data["destinations"][0]
        assert "id" in first
        assert "name" in first
        assert "country" in first
        assert "climate" in first


def test_get_specific_destination_success(test_client):
    # Assuming at least one destination exists (id=1)
    response = test_client.get("travel/api/destinations/1")
    if response.status_code == 404:
        pytest.skip("Destination with id=1 not found in test DB.")
    else:
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["id"] == 1
        assert "name" in data
        assert "country" in data


def test_get_nonexistent_destination_returns_404(test_client):
    # Use a very large ID unlikely to exist
    response = test_client.get("travel/api/destinations/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Destination not found"
