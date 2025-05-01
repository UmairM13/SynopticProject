import pytest
from fastapi.testclient import TestClient
from recommendation_engine.api.main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def test_client():
    return client

def test_top_destinations(test_client):
    response = test_client.get("/travel/api/analytics/top-destinations")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert "destination_name" in data[0]
        assert "count" in data[0]

def test_user_stats(test_client):
    response = test_client.get("/travel/api/analytics/user-stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_users" in data
    assert "avg_age" in data
    assert "avg_budget" in data
    assert "avg_trip_duration" in data
    assert "top_climate" in data
    assert "top_terrain" in data
    assert "top_holiday_type" in data
    assert "top_nationalities" in data
    assert "total_recommendations" in data

def test_recommendation_activity(test_client):
    response = test_client.get("/travel/api/analytics/recommendation-activity")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert "year" in data[0]
        assert "month" in data[0]
        assert "count" in data[0]

def test_preferences_distribution(test_client):
    response = test_client.get("/travel/api/analytics/preferences-distribution")
    assert response.status_code == 200
    data = response.json()
    assert "climates" in data
    assert "terrains" in data
    if data["climates"]:
        assert "climate" in data["climates"][0]
        assert "count" in data["climates"][0]
    if data["terrains"]:
        assert "terrain" in data["terrains"][0]
        assert "count" in data["terrains"][0]

def test_past_destinations_by_age(test_client):
    response = test_client.get("/travel/api/analytics/past-destinations-by-age")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert "age" in data[0]
        assert "destination" in data[0]
        assert "count" in data[0]

def test_past_destinations_by_nationality(test_client):
    response = test_client.get("/travel/api/analytics/past-destinations-by-nationality")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert "nationality" in data[0]
        assert "destination" in data[0]
        assert "count" in data[0]

def test_off_season_rate(test_client):
    response = test_client.get("/travel/api/analytics/off-season-rate")
    assert response.status_code == 200
    data = response.json()
    assert "off_season_recommendations" in data
    assert "peak_season_recommendations" in data
    assert "off_season_ratio" in data

def test_off_season_monthly(test_client):
    response = test_client.get("/travel/api/analytics/off-season-monthly")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert "month" in data[0]
        assert "off_season_destinations" in data[0]
