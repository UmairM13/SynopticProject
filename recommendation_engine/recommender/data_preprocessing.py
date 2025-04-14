import pandas as pd
import os
import pickle
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from data_collection import users_df, destinations_df  # Load cleaned data
from datetime import datetime

# Define categorical features for encoding
one_hot_features = ["country", "climate", "terrain", "language"]
label_feature = "holiday_type"

# One-Hot Encoding for categorical features
ohe = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
encoded_df = pd.DataFrame(ohe.fit_transform(destinations_df[one_hot_features]))
encoded_df.columns = ohe.get_feature_names_out(one_hot_features)

# Merge encoded features
destinations_df = destinations_df.drop(columns=one_hot_features)
destinations_df = pd.concat([destinations_df, encoded_df], axis=1)

# Label Encoding for holiday_type - using one-hot instead of label encoding for better recommendations
if label_feature in users_df.columns:
    users_df[label_feature] = users_df[label_feature].fillna("Unknown")
    holiday_encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    holiday_encoded = pd.DataFrame(
        holiday_encoder.fit_transform(users_df[[label_feature]]),
        columns=holiday_encoder.get_feature_names_out([label_feature])
    )
    users_df = pd.concat([users_df, holiday_encoded], axis=1)

# Add off-season preference feature
current_month = datetime.now().month

# Create off-season score for destinations
def calculate_off_season_score(row):
    # If off-season data is present
    if pd.notna(row.get("off_season_start")) and pd.notna(row.get("off_season_end")):
        start = int(row["off_season_start"])
        end = int(row["off_season_end"])
        
        # Check if current month is in off-season period
        if start <= end:
            is_off_season = start <= current_month <= end
        else:  # Handles cases where off-season spans year end (e.g., Nov-Feb)
            is_off_season = current_month >= start or current_month <= end
            
        # Assign higher score for off-season destinations
        return 1.0 if is_off_season else 0.5
    return 0.5  # Default value if no off-season data

destinations_df["off_season_score"] = destinations_df.apply(calculate_off_season_score, axis=1)

# Normalize numerical features for better model performance
numerical_features = ["avg_daily_budget", "flight_cost", "hotel_cost"]
scaler = StandardScaler()

# Scale only if columns exist
existing_num_cols = [col for col in numerical_features if col in destinations_df.columns]
if existing_num_cols:
    destinations_df[existing_num_cols] = scaler.fit_transform(
        destinations_df[existing_num_cols].fillna(0)
    )

# Save processed data
base_dir = os.path.dirname(os.path.abspath(__file__))
save_dir = os.path.join(base_dir, "processed_data")
os.makedirs(save_dir, exist_ok=True)

# Save all preprocessing tools
with open(os.path.join(save_dir, "preprocessors.pkl"), "wb") as f:
    pickle.dump({
        "one_hot": ohe,
        "holiday_encoder": holiday_encoder if label_feature in users_df.columns else None,
        "scaler": scaler if existing_num_cols else None,
        "current_month": current_month
    }, f)

destinations_df.to_pickle(os.path.join(save_dir, "processed_destinations.pkl"))
users_df.to_pickle(os.path.join(save_dir, "processed_users.pkl"))

print("Preprocessing complete. Processed data saved.")
print(f"Current month: {current_month} - Off-season preferences applied to recommendations.")