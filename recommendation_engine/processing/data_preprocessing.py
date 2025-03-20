import pandas as pd
import os
import pickle
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

# Load cleaned data from data_loading.py
from data_loading import users_df, destinations_df, travel_costs_df

# One-Hot Encoding for categorical features
ohe_features = ['country', 'climate', 'terrain', 'language']
encoder = OneHotEncoder(sparse=False, drop='first')  # Avoid multicollinearity

encoded_df = pd.DataFrame(encoder.fit_transform(destinations_df[ohe_features]))
encoded_df.columns = encoder.get_feature_names_out(ohe_features)

# Drop original columns and concatenate encoded ones
destinations_df = destinations_df.drop(columns=ohe_features)
destinations_df = pd.concat([destinations_df, encoded_df], axis=1)

# Label Encoding for ordinal categorical features
label_encoder = LabelEncoder()
destinations_df['holiday_type_encoded'] = label_encoder.fit_transform(destinations_df['holiday_type'])
destinations_df.drop(columns=['holiday_type'], inplace=True)

# Save the encoders for future use
with open("encoders.pkl", "wb") as f:
    pickle.dump({'one_hot': encoder, 'label': label_encoder}, f)

# Save the processed DataFrame for further use
processed_file = "processed_data.pkl"
destinations_df.to_pickle(processed_file)

print("Preprocessing complete. Encoded data saved to:", processed_file)
