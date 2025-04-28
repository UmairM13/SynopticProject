import os
import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler, MultiLabelBinarizer

# Dynamically load data
from recommendation_engine.recommender.data_collection import users_df, destinations_df, past_destinations_df
from recommendation_engine.recommender.data_loader import load_processed_data
from recommendation_engine.recommender.data_loader import DataManager

# # For testing
# from data_collection import users_df, destinations_df, past_destinations_df
# from data_loader import load_processed_data
# from data_loader import DataManager

def encode_multi_label(df, column, prefix):
    mlb = MultiLabelBinarizer()
    df[column] = df[column].apply(lambda x: [item.strip() for item in x.split(",")] if isinstance(x, str) else [])
    encoded = pd.DataFrame(mlb.fit_transform(df[column]), columns=[f"{prefix}_{cls}" for cls in mlb.classes_])
    return df.drop(columns=[column]), encoded, mlb

def one_hot_encode(df, features):
    ohe = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    encoded = pd.DataFrame(ohe.fit_transform(df[features]))
    encoded.columns = ohe.get_feature_names_out(features)
    return encoded, ohe


def safe_encode_multi_label(df, column, prefix):
    if column not in df.columns:
        print(f"[Warning] Column '{column}' not found in DataFrame. Skipping.")
        return df, pd.DataFrame(), None
    return encode_multi_label(df, column, prefix)


def scale_numerical(df, num_cols):
    scaler = StandardScaler()
    df[num_cols] = df[num_cols].fillna(df[num_cols].median())
    for col in num_cols:
        df[f"{col}_original"] = df[col]
    df[num_cols] = scaler.fit_transform(df[num_cols])
    return df, scaler

def save_processed(users_df, destinations_df, preprocessors):
    path = os.path.join(os.path.dirname(__file__), "processed_data")
    os.makedirs(path, exist_ok=True)

    # Delete all old files first
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

    # Save fresh
    with open(os.path.join(path, "preprocessors.pkl"), "wb") as f:
        pickle.dump(preprocessors, f)

    users_df.to_pickle(os.path.join(path, "processed_users.pkl"))
    destinations_df.to_pickle(os.path.join(path, "processed_destinations.pkl"))
    past_destinations_df.to_pickle(os.path.join(path, "processed_past_destinations.pkl"))

    # also save CSVs for easier debugging
    users_df.to_csv(os.path.join(path, "processed_users.csv"), index=False)
    destinations_df.to_csv(os.path.join(path, "processed_destinations.csv"), index=False)
    past_destinations_df.to_csv(os.path.join(path, "processed_past_destinations.csv"), index=False)


def run_preprocessing():
    global users_df, destinations_df, past_destinations_df

    from recommendation_engine.recommender.data_collection import users_df as fresh_users_df, destinations_df as fresh_destinations_df, past_destinations_df as fresh_past_destinations_df
    # from data_collection import users_df as fresh_users_df, destinations_df as fresh_destinations_df, past_destinations_df as fresh_past_destinations_df

    users_df = fresh_users_df.copy()
    destinations_df = fresh_destinations_df.copy()
    past_destinations_df = fresh_past_destinations_df.copy()
    
    
    # --- Destinations ---
    destinations_df, climate_encoded, climate_mlb = safe_encode_multi_label(destinations_df, "climate", "climate")
    destinations_df, terrain_encoded, terrain_mlb = safe_encode_multi_label(destinations_df, "terrain", "terrain")
    destinations_df, holiday_encoded, holiday_mlb = safe_encode_multi_label(destinations_df, "holiday_type", "holiday_type")

    one_hot_features = ["country", "language"]
    one_hot_encoded, ohe = one_hot_encode(destinations_df, one_hot_features)
    destinations_df = destinations_df.drop(columns=one_hot_features)

    destinations_df = pd.concat([
        destinations_df,
        climate_encoded,
        terrain_encoded,
        holiday_encoded,
        one_hot_encoded
    ], axis=1)

    destinations_df, scaler = scale_numerical(destinations_df, ["avg_daily_budget", "flight_cost", "hotel_cost"])

    # --- Users ---
    users_df['preferred_climate_original'] = users_df['preferred_climate']
    users_df['preferred_terrain_original'] = users_df['preferred_terrain']
    users_df['holiday_type_original'] = users_df['holiday_type']
    users_df, user_climate_encoded, user_climate_mlb = encode_multi_label(users_df, "preferred_climate", "preferred_climate")
    users_df, user_terrain_encoded, user_terrain_mlb = encode_multi_label(users_df, "preferred_terrain", "preferred_terrain")
    users_df, user_holiday_encoded, user_holiday_mlb = encode_multi_label(users_df, "holiday_type", "holiday_type")

    users_df = pd.concat([
        users_df,
        user_climate_encoded,
        user_terrain_encoded,
        user_holiday_encoded
    ], axis=1)

    # --- Past Destinations ---
    past_destinations_df["trip_end_date"] = pd.to_datetime(past_destinations_df["trip_end_date"], errors='coerce')
    past_destinations_df.dropna(subset=["trip_end_date", "destination_name"], inplace=True)
    past_destinations_df.sort_values(by=["user_id", "trip_end_date"], ascending=[True, False], inplace=True)

    # Save
    preprocessors = {
        "one_hot": ohe,
        "scaler": scaler,
        "climate_mlb": climate_mlb,
        "terrain_mlb": terrain_mlb,
        "holiday_mlb": holiday_mlb,
        "user_climate_mlb": user_climate_mlb,
        "user_terrain_mlb": user_terrain_mlb,
        "user_holiday_mlb": user_holiday_mlb,
    }

    save_processed(users_df, destinations_df, preprocessors)

    # 🚀 Then reload DataManager cache clean again
    data_manager = DataManager.get_instance()
    data_manager.refresh()
    return {
        "status": "success",
        "message": "Preprocessing completed and saved.",
        "users_loaded": len(data_manager.get_users()),
        "destinations_loaded": len(data_manager.get_destinations())
    }
    
    
if __name__ == "__main__":
    
    print(run_preprocessing())
