from recommendation_engine.recommender.data_collection import fetch_fresh_data


def test_fetch_fresh_data():
    users_df, destinations_df, past_destinations_df = fetch_fresh_data()
    assert not users_df.empty
    assert not destinations_df.empty
    assert not past_destinations_df.empty
    
 