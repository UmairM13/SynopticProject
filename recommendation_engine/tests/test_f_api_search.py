import pytest
from fastapi.testclient import TestClient
from recommendation_engine.api.main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def test_client():
    return client

def test_search_similar(test_client):
    response = test_client.get("/travel/api/search/search-similar", params={"destination_name": "Paris"})
    assert response.status_code in [200, 404]  # 404 if destination not found
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, list)
        if data:
            assert "id" in data[0]
            assert "name" in data[0]

def test_get_popular_destinations(test_client):
    response = test_client.get("/travel/api/search/popular-destinations")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert "id" in data[0]
        assert "name" in data[0]

def test_search_destinations(test_client):
    # We assume destinations like "Paris" or "Tokyo" exist in dummy data
    response = test_client.get("/travel/api/search/search", params={"query": "Paris"})
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert isinstance(data["results"], list)
    if data["results"]:
        first_result = data["results"][0]
        assert "id" in first_result
        assert "name" in first_result
        assert "country" in first_result
        assert "avg_daily_budget" in first_result
