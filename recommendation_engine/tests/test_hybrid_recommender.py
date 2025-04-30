import pytest
import pandas as pd
from recommendation_engine.recommender.hybrid_recommender import recommend_destinations
from recommendation_engine.recommender.data_loader import load_processed_data

@pytest.fixture(scope="module")
def loaded_data():
    users_df, destinations_df, past_destinations_df = load_processed_data()
    return users_df, destinations_df, past_destinations_df

def test_recommendations_not_empty(loaded_data):
    users_df, destinations_df, past_destinations_df = loaded_data
    user_id = users_df["id"].iloc[0]
    recs = recommend_destinations(user_id, users_df, destinations_df, past_destinations_df)
    assert not recs.empty, "Recommendations should not be empty"

def test_recommendations_have_required_columns(loaded_data):
    users_df, destinations_df, past_destinations_df = loaded_data
    user_id = users_df["id"].iloc[0]
    recs = recommend_destinations(user_id, users_df, destinations_df, past_destinations_df)

    expected_cols = {"id", "name", "country", "final_score", "knn_score", 
                     "similarity_score", "past_similarity", "off_season_score", 
                     "avg_daily_budget", "is_off_season"}
    assert expected_cols.issubset(recs.columns), "Missing required columns in recommendations"

def test_final_scores_in_expected_range(loaded_data):
    users_df, destinations_df, past_destinations_df = loaded_data
    user_id = users_df["id"].iloc[0]
    recs = recommend_destinations(user_id, users_df, destinations_df, past_destinations_df)

    assert recs["final_score"].between(0, 1.5).all(), "Final scores should be roughly between 0 and 1.5"

def test_knn_scores_non_negative(loaded_data):
    users_df, destinations_df, past_destinations_df = loaded_data
    user_id = users_df["id"].iloc[0]
    recs = recommend_destinations(user_id, users_df, destinations_df, past_destinations_df)

    assert (recs["knn_score"] >= 0).all(), "KNN scores must be non-negative"

def test_similarity_scores_range(loaded_data):
    users_df, destinations_df, past_destinations_df = loaded_data
    user_id = users_df["id"].iloc[0]
    recs = recommend_destinations(user_id, users_df, destinations_df, past_destinations_df)

    assert recs["similarity_score"].between(0, 1).all(), "Similarity scores must be between 0 and 1"

def test_past_similarity_scores_range(loaded_data):
    users_df, destinations_df, past_destinations_df = loaded_data
    user_id = users_df["id"].iloc[0]
    recs = recommend_destinations(user_id, users_df, destinations_df, past_destinations_df)

    assert recs["past_similarity"].between(0, 1).all(), "Past similarity scores must be between 0 and 1"

def test_off_season_labels_correct(loaded_data):
    users_df, destinations_df, past_destinations_df = loaded_data
    user_id = users_df["id"].iloc[0]
    recs = recommend_destinations(user_id, users_df, destinations_df, past_destinations_df)

    allowed_labels = {"Yes", "No"}
    assert recs["is_off_season"].isin(allowed_labels).all(), "'is_off_season' must be 'Yes' or 'No'"

def test_user_not_found_case(loaded_data):
    users_df, destinations_df, past_destinations_df = loaded_data
    fake_user_id = 999999  # Assuming this ID does not exist
    recs = recommend_destinations(fake_user_id, users_df, destinations_df, past_destinations_df)

    assert recs == "User not found", "Should return 'User not found' for invalid user IDs"

def test_default_number_of_recommendations(loaded_data):
    users_df, destinations_df, past_destinations_df = loaded_data
    user_id = users_df["id"].iloc[0]
    recs = recommend_destinations(user_id, users_df, destinations_df, past_destinations_df)

    assert len(recs) <= 20, "Should return up to 20 recommendations by default"
