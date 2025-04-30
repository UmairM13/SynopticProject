from recommendation_engine.recommender.collaborative_model import train_collaborative_model, collab_recommendations
from recommendation_engine.recommender.data_loader import load_processed_data
import pandas as pd

def test_train_collaborative_model():
    model = train_collaborative_model()
    assert model is not None

def test_collaborative_recommendations():
    model = train_collaborative_model()
    if model:
        users_df, destinations_df, past_destinations_df = load_processed_data()
        user_id = users_df["id"].iloc[0]
        recommendations = collab_recommendations(user_id, model)
        assert isinstance(recommendations, pd.DataFrame)