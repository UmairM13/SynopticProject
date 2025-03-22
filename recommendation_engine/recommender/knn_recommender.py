import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from data_loader import destinations_df, users_df

# Check available columns
print("Columns in destinations_df:", destinations_df.columns)

# Convert datetime columns to numerical values (if they exist)
if 'off_season_start' in destinations_df.columns:
    destinations_df['off_season_start'] = pd.to_datetime(destinations_df['off_season_start']).astype(int) / 10**9  
if 'off_season_end' in destinations_df.columns:
    destinations_df['off_season_end'] = pd.to_datetime(destinations_df['off_season_end']).astype(int) / 10**9

# Exclude non-numeric columns
drop_columns = ['id', 'name', 'country', 'currency']  # Exclude non-numeric columns
features = destinations_df.drop(columns=[col for col in drop_columns if col in destinations_df.columns])

# Ensure all feature columns are numeric
features = features.apply(pd.to_numeric, errors='coerce')

# Handle missing values
if features.isnull().values.any():
    print("\nWarning: Missing values detected. Filling with column means.")
    features.fillna(features.mean(), inplace=True)  # Replace NaNs with column means

# Fit the KNN model
knn = NearestNeighbors(n_neighbors=5, metric='euclidean')
knn.fit(features)

def recommend_destinations(user_id, n_recommendations=5):
    """Recommend destinations based on user preferences, nationality, climate, and terrain."""
    user = users_df[users_df['id'] == user_id]

    if user.empty:
        return "User not found."

    # Extract numerical user preferences
    user_features = {
        'budget': user['budget'].values[0],
        'holiday_type_encoded': user['holiday_type_encoded'].values[0]
    }

    # Add one-hot encoding for nationality
    nationality_column = f"country_{user['nationality'].values[0]}"
    if nationality_column in features.columns:
        user_features[nationality_column] = 1

    # Add one-hot encoding for preferred climate
    # climate_column = f"climate_{user['preferred_climate'].values[0]}"
    # if climate_column in features.columns:
    #     user_features[climate_column] = 1

    # # Add one-hot encoding for preferred terrain
    # terrain_column = f"terrain_{user['preferred_terrain'].values[0]}"
    # if terrain_column in features.columns:
    #     user_features[terrain_column] = 1

    # Convert user features to match feature columns in destinations_df
    user_vector = pd.Series(0, index=features.columns)  # Initialize with zeros
    for key, value in user_features.items():
        if key in user_vector:
            user_vector[key] = value

    # Reshape user vector to match expected input format
    user_vector = user_vector.values.reshape(1, -1)

    # Find similar destinations
    distances, indices = knn.kneighbors(user_vector, n_neighbors=n_recommendations)

    # Ensure we only return valid columns
    return_columns = ['name'] if 'name' in destinations_df.columns else destinations_df.columns[:1]
    recommendations = destinations_df.iloc[indices[0]][return_columns]
    
    return recommendations

# Example usage
if __name__ == "__main__":
    user_id = 4  # Change for different users
    print(recommend_destinations(user_id))
