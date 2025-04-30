import os
from recommendation_engine.recommender.data_preprocessing import run_preprocessing


def test_run_preprocessing_creates_files():
    run_preprocessing()
    processed_path = os.path.join(os.path.dirname(__file__), '../../recommendation_engine/recommender/processed_data')
    assert os.path.exists(os.path.join(processed_path, 'users.pkl'))