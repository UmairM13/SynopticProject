import pandas as pd
import pickle
import os

# Define paths
DATA_DIR = os.path.join(os.path.dirname(__file__), "processed_data")

# Load processed data
destinations_path = os.path.join(DATA_DIR, "processed_destinations.pkl")
users_path = os.path.join(DATA_DIR, "processed_users.pkl")

if os.path.exists(destinations_path) and os.path.exists(users_path):
    destinations_df = pd.read_pickle(destinations_path)
    users_df = pd.read_pickle(users_path)
    print("Processed data successfully loaded!")
else:
    raise FileNotFoundError("Processed data files not found. Ensure preprocessing was completed.")
