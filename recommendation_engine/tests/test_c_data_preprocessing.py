import os
import pytest
import pandas as pd
import pickle

from recommendation_engine.recommender import data_preprocessing


@pytest.fixture(scope="module")
def preprocessing_output():
    # Run preprocessing once for the module
    result = data_preprocessing.run_preprocessing()
    return result


def test_preprocessing_status(preprocessing_output):
    assert preprocessing_output["status"] == "success"
    assert preprocessing_output["users_loaded"] > 0
    assert preprocessing_output["destinations_loaded"] > 0


def test_processed_files_exist():
    path = os.path.join(os.path.dirname(data_preprocessing.__file__), "processed_data")
    assert os.path.exists(path)
    assert os.path.isfile(os.path.join(path, "processed_users.pkl"))
    assert os.path.isfile(os.path.join(path, "processed_destinations.pkl"))
    assert os.path.isfile(os.path.join(path, "processed_past_destinations.pkl"))
    assert os.path.isfile(os.path.join(path, "preprocessors.pkl"))


def test_loaded_processed_users():
    path = os.path.join(os.path.dirname(data_preprocessing.__file__), "processed_data", "processed_users.pkl")
    users_df = pd.read_pickle(path)
    assert isinstance(users_df, pd.DataFrame)
    assert "email" in users_df.columns or "id" in users_df.columns


def test_loaded_processed_destinations():
    path = os.path.join(os.path.dirname(data_preprocessing.__file__), "processed_data", "processed_destinations.pkl")
    dest_df = pd.read_pickle(path)
    assert isinstance(dest_df, pd.DataFrame)
    assert "name" in dest_df.columns or "id" in dest_df.columns


def test_loaded_preprocessors():
    path = os.path.join(os.path.dirname(data_preprocessing.__file__), "processed_data", "preprocessors.pkl")
    with open(path, "rb") as f:
        preprocessors = pickle.load(f)
    assert "one_hot" in preprocessors
    assert "scaler" in preprocessors
    assert "climate_mlb" in preprocessors
