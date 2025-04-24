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