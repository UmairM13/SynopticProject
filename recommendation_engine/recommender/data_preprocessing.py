import pandas as pd
import os
import pickle
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from data_collection import users_df, destinations_df  # Load cleaned data

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

# Label Encoding for holiday_type
label_encoder = LabelEncoder()
if label_feature in users_df.columns:
    users_df[label_feature] = users_df[label_feature].fillna("Unknown")  # Avoid FutureWarning
    users_df["holiday_type_encoded"] = label_encoder.fit_transform(users_df[label_feature])
    users_df.drop(columns=[label_feature], inplace=True)

# Save processed data
base_dir = os.path.dirname(os.path.abspath(__file__))
save_dir = os.path.join(base_dir, "processed_data")
os.makedirs(save_dir, exist_ok=True)

with open(os.path.join(save_dir, "encoders.pkl"), "wb") as f:
    pickle.dump({"one_hot": ohe, "label": label_encoder}, f)

destinations_df.to_pickle(os.path.join(save_dir, "processed_destinations.pkl"))
users_df.to_pickle(os.path.join(save_dir, "processed_users.pkl"))

print("Preprocessing complete. Processed data saved.")
