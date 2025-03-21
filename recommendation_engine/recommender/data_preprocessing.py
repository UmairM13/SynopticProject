import pandas as pd
import os
import pickle
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

# Load cleaned data from data_loading.py
from data_collection import users_df, destinations_df, travel_costs_df

# One-Hot Encoding for categorical features
ohe_features = ['country', 'climate', 'terrain', 'language']
encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")  # Avoid multicollinearity

encoded_df = pd.DataFrame(encoder.fit_transform(destinations_df[ohe_features]))
encoded_df.columns = encoder.get_feature_names_out(ohe_features)

# Drop original columns and concatenate encoded ones
destinations_df = destinations_df.drop(columns=ohe_features)
destinations_df = pd.concat([destinations_df, encoded_df], axis=1)

# Label Encoding for ordinal categorical features
label_encoder = LabelEncoder()

# Check if 'holiday_type' exists in destinations_df, otherwise use users_df
if 'holiday_type' in destinations_df.columns:
    destinations_df['holiday_type'].fillna('Unknown', inplace=True)  # Handle missing values
    destinations_df['holiday_type_encoded'] = label_encoder.fit_transform(destinations_df['holiday_type'])
    destinations_df.drop(columns=['holiday_type'], inplace=True)
elif 'holiday_type' in users_df.columns:
    users_df['holiday_type'].fillna('Unknown', inplace=True)  # Handle missing values
    users_df['holiday_type_encoded'] = label_encoder.fit_transform(users_df['holiday_type'])
    users_df.drop(columns=['holiday_type'], inplace=True)
    print("Applied encoding to users_df instead of destinations_df.")
else:
    print("Warning: 'holiday_type' column not found in either DataFrame!")

# Define save path as the script's directory
base_dir = os.path.dirname(os.path.abspath(__file__))
save_dir = os.path.join(base_dir, "processed_data")
os.makedirs(save_dir, exist_ok=True)
processed_dest_file = os.path.join(save_dir, "processed_destinations.pkl")
processed_users_file = os.path.join(save_dir, "processed_users.pkl")

# Save the encoders for future use
with open(os.path.join(save_dir, "encoders.pkl"), "wb") as f:
    pickle.dump({'one_hot': encoder, 'label': label_encoder}, f)

# Save the processed DataFrames for further use
destinations_df.to_pickle(processed_dest_file)
users_df.to_pickle(processed_users_file)

print("Preprocessing complete. Encoded data saved to:", processed_dest_file, "and", processed_users_file)
