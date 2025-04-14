import pandas as pd
import pickle
import os

def load_processed_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    save_dir = os.path.join(base_dir, "processed_data")
    
    destinations = pd.read_pickle(os.path.join(save_dir, "processed_destinations.pkl"))
    users = pd.read_pickle(os.path.join(save_dir, "processed_users.pkl"))
    
    return destinations, users

# Make DataFrames available for direct import
destinations_df, users_df = load_processed_data()