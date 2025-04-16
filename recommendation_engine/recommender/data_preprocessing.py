import pandas as pd
import os
import pickle
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler, MultiLabelBinarizer


def encode_climate(destinations_df):
    mlb = MultiLabelBinarizer()
    destinations_df['climate'] = destinations_df['climate'].str.split(',')
    climate_encoded = pd.DataFrame(
        mlb.fit_transform(destinations_df['climate']),
        columns=[f"climate_{c}" for c in mlb.classes_]
    )
    return destinations_df.drop(columns=['climate']), climate_encoded, mlb


def one_hot_encode(df, features):
    ohe = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    encoded = pd.DataFrame(ohe.fit_transform(df[features]))
    encoded.columns = ohe.get_feature_names_out(features)
    return encoded, ohe


def scale_numerical(df, num_cols):
    df = df.copy()
    scaler = StandardScaler()
    for col in num_cols:
        df[f"{col}_original"] = df[col]
    df[num_cols] = df[num_cols].fillna(df[num_cols].median())
    df[num_cols] = scaler.fit_transform(df[num_cols])
    return df, scaler


def save_processed(users_df, destinations_df, preprocessors):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    save_dir = os.path.join(base_dir, "processed_data")
    os.makedirs(save_dir, exist_ok=True)
    
    # Clean up old files
    for file in os.listdir(save_dir):
        file_path = os.path.join(save_dir, file)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Warning: Failed to delete {file_path} - {e}")
            
    # Save new files
    with open(os.path.join(save_dir, "preprocessors.pkl"), "wb") as f:
        pickle.dump(preprocessors, f)

    destinations_df.to_pickle(os.path.join(save_dir, "processed_destinations.pkl"))
    users_df.to_pickle(os.path.join(save_dir, "processed_users.pkl"))
    
    users_df_csv = users_df.copy()
    users_df_csv['past_destinations'] = users_df_csv['past_destinations'].apply(str)
    users_df_csv.to_csv(os.path.join(save_dir, "processed_users.csv"), index=False)
    destinations_df.to_csv(os.path.join(save_dir, "processed_destinations.csv"), index=False)

def run_preprocessing():
    global users_df, destinations_df
    
    from recommendation_engine.recommender.data_collection import users_df, destinations_df
    from datetime import datetime

    destinations_df, climate_encoded, mlb = encode_climate(destinations_df)
    one_hot_features = ["country", "terrain", "language"]
    encoded_df, ohe = one_hot_encode(destinations_df, one_hot_features)

    destinations_df = destinations_df.drop(columns=one_hot_features)
    destinations_df = pd.concat([destinations_df, climate_encoded, encoded_df], axis=1)

    destinations_df, scaler = scale_numerical(destinations_df, ["avg_daily_budget", "flight_cost", "hotel_cost"])

    preprocessors = {
        "one_hot": ohe,
        "scaler": scaler,
        "climate_mlb": mlb
    }

    save_processed(users_df, destinations_df, preprocessors)
    
    # Reload fresh version after saving to disk
    from recommendation_engine.recommender.data_loader import load_processed_data

    users_df, destinations_df = load_processed_data()


    return {"status": "success", "message": "Preprocessing completed and saved."}


if __name__ == "__main__":
    run_preprocessing()
    print("Preprocessing completed and saved.")