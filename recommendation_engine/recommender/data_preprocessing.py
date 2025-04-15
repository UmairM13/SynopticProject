import pandas as pd
import os
import pickle
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler, MultiLabelBinarizer
from data_collection import users_df, destinations_df  # Load cleaned data
from datetime import datetime
import re
import ast

# Define categorical features for encoding
one_hot_features = ["country", "terrain", "language"]
label_feature = "holiday_type"

destinations_df['climate'] = destinations_df['climate'].str.split(',')

mlb = MultiLabelBinarizer()
climate_encoded = pd.DataFrame(
    mlb.fit_transform(destinations_df['climate']),
    columns=[f"climate_{c}" for c in mlb.classes_]
)

# One-Hot Encoding for categorical features
ohe = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
encoded_df = pd.DataFrame(ohe.fit_transform(destinations_df[one_hot_features]))
encoded_df.columns = ohe.get_feature_names_out(one_hot_features)

# Merge encoded features
destinations_df = destinations_df.drop(columns=one_hot_features + ['climate'])
destinations_df = pd.concat([destinations_df, climate_encoded, encoded_df], axis=1)

print("Original past_destinations values:")
print(users_df['past_destinations'].head(10))

print(users_df['past_destinations'].head())
print(type(users_df['past_destinations'].iloc[0]))

def clean_past_destinations(x):
    if isinstance(x, list):
        return x  # already good
    if pd.isna(x) or not isinstance(x, str):
        return []
    # Remove square brackets and extra spaces
    x = x.strip().strip('[]')
    return [item.strip() for item in x.split(',') if item.strip()]

users_df['past_destinations'] = users_df['past_destinations'].apply(clean_past_destinations)

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


# Normalize numerical features for better model performance
numerical_features = ["avg_daily_budget", "flight_cost", "hotel_cost"]
existing_num_cols = [col for col in numerical_features if col in destinations_df.columns]

# Fill with median instead of mean
if existing_num_cols:
    destinations_df[existing_num_cols] = destinations_df[existing_num_cols].fillna(
        destinations_df[existing_num_cols].median()
    )
    scaler = StandardScaler()
    destinations_df[existing_num_cols] = scaler.fit_transform(destinations_df[existing_num_cols])
    
    
# Scale only if columns exist
existing_num_cols = [col for col in numerical_features if col in destinations_df.columns]
if existing_num_cols:
    destinations_df[existing_num_cols] = scaler.fit_transform(
        destinations_df[existing_num_cols].fillna(0)
    )
    

# Before saving processed data
print("Final columns in users_df:", users_df.columns.tolist())
print("past_destinations present:", 'past_destinations' in users_df.columns)
print("past_destinations sample:", users_df['past_destinations'].head())

# Save processed data
base_dir = os.path.dirname(os.path.abspath(__file__))
save_dir = os.path.join(base_dir, "processed_data")
os.makedirs(save_dir, exist_ok=True)

# Save all preprocessing tools
with open(os.path.join(save_dir, "preprocessors.pkl"), "wb") as f:
    pickle.dump({
        "one_hot": ohe,
        "holiday_encoder": holiday_encoder if label_feature in users_df.columns else None,
        "scaler": scaler if existing_num_cols else None
    }, f)

destinations_df.to_pickle(os.path.join(save_dir, "processed_destinations.pkl"))
users_df.to_pickle(os.path.join(save_dir, "processed_users.pkl"))
# Also save as CSV for better compatibility
destinations_df.to_csv(os.path.join(save_dir, "processed_destinations.csv"), index=False)
# Save users_df as CSV, but with past_destinations as string
users_df_csv = users_df.copy()
users_df_csv['past_destinations'] = users_df_csv['past_destinations'].apply(str)
users_df_csv.to_csv(os.path.join(save_dir, "processed_users.csv"), index=False)

print("Preprocessing complete. Processed data saved.")