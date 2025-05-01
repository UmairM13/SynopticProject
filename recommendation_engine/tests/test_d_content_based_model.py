from recommendation_engine.recommender.content_based_model import prepare_features, recommend_similar_destinations
from recommendation_engine.recommender.data_loader import load_processed_data
import pandas as pd

def test_content_recommendation():
    _, destinations_df, _ = load_processed_data()
    features_df, similarity_matrix = prepare_features(destinations_df)
    recommendations = recommend_similar_destinations("London", destinations_df, features_df, similarity_matrix, top_n=5)
    assert isinstance(recommendations, pd.DataFrame)