import pandas as pd
import pickle
import numpy as np
import os

def load_processed_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    save_dir = os.path.join(base_dir, "processed_data")
    
    destinations = pd.read_pickle(os.path.join(save_dir, "processed_destinations.pkl"))
    users = pd.read_pickle(os.path.join(save_dir, "processed_users.pkl"))
    past_destinations = pd.read_pickle(os.path.join(save_dir, "processed_past_destinations.pkl"))
    
    users = users.copy()
    destinations = destinations.copy()
    past_destinations = past_destinations.copy()

    users_numeric = users.select_dtypes(include=[np.number]).columns
    users[users_numeric] = users[users_numeric].fillna(0)

    dest_numeric = destinations.select_dtypes(include=[np.number]).columns
    destinations[dest_numeric] = destinations[dest_numeric].fillna(0)

    return users, destinations, past_destinations


# NEW: Singleton-like helper to always refresh from disk
class DataManager:
    _instance = None

    def __init__(self):
        self.refresh()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def refresh(self):
        from recommendation_engine.recommender.data_loader import load_processed_data
        self.users_df, self.destinations_df, self.past_destinations_df = load_processed_data()

    def get_users(self):
        return self.users_df

    def get_destinations(self):
        return self.destinations_df

    def get_past_destinations(self):
        return self.past_destinations_df