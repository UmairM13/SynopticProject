import pandas as pd
import numpy as np
from decimal import Decimal
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from data_loader import destinations_df, users_df

# Check available columns
print("Columns in destinations_df:", destinations_df.columns)

# Convert off-season months to numerical values (Ensure they are within valid month range)
if 'off_season_start' in destinations_df.columns:
    destinations_df['off_season_start'] = pd.to_datetime(destinations_df['off_season_start'], errors='coerce').dt.month
if 'off_season_end' in destinations_df.columns:
    destinations_df['off_season_end'] = pd.to_datetime(destinations_df['off_season_end'], errors='coerce').dt.month

# Drop non-numeric columns for model training
drop_columns = ['id', 'name', 'currency']
features = destinations_df.drop(columns=[col for col in drop_columns if col in destinations_df.columns])

# Ensure all feature columns are numeric
features = features.apply(pd.to_numeric, errors='coerce')

# Handle missing values (mean for numerical, mode for categorical)
for col in features.columns:
    if features[col].dtype == 'object':  # Categorical columns
        features[col] = features[col].fillna(features[col].mode()[0])
    else:  # Numerical columns
        features[col] = features[col].fillna(features[col].mean())

# Normalize features using StandardScaler
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# Fit the KNN model with increased neighbors
n_neighbors = 10  # Increase the number of neighbors
knn = NearestNeighbors(n_neighbors=n_neighbors, metric='euclidean')
knn.fit(features_scaled)

def recommend_destinations(user_id, n_recommendations=5, weight_kNN=0.6, weight_similarity=0.4):
    user = users_df[users_df['id'] == user_id]
    
    if user.empty:
        return "User ID not found in the database."

    # Initialize user vector with zeros based on features
    user_vector = pd.DataFrame(0, index=[0], columns=features.columns)

    # Set budget
    user_vector['avg_daily_budget'] = user['budget'].values[0]

    # Handle one-hot encoding for user preferences with respect to existing columns in features
    def set_one_hot_encoding(preference, column_prefix, user_vector):
        if pd.notna(preference):
            column_name = f"{column_prefix}_{preference}"
            if column_name in user_vector.columns:
                user_vector[column_name] = 1

    # One-hot encoding for nationality
    set_one_hot_encoding(user['nationality'].values[0], "country", user_vector)
    # One-hot encoding for preferred climate
    set_one_hot_encoding(user['preferred_climate'].values[0], "climate", user_vector)
    # One-hot encoding for preferred terrain
    set_one_hot_encoding(user['preferred_terrain'].values[0], "terrain", user_vector)

    # Ensure user_vector retains column names before kneighbors()
    user_vector = pd.DataFrame(user_vector, columns=features.columns)
    # Normalize the user vector
    user_vector_scaled = scaler.transform(user_vector)

    # Find the nearest destinations using KNN
    distances, indices = knn.kneighbors(user_vector_scaled, n_neighbors=n_recommendations)

    # Updated similarity function that uses one-hot encoded columns for climate and terrain
    def calculate_similarity(destination, user):
        similarity_score = 0

        # Check for climate match using one-hot encoding
        user_climate = user['preferred_climate'].values[0]
        climate_col = f"climate_{user_climate}"
        if climate_col in destination.index and destination[climate_col] == 1:
            similarity_score += 1
            print("Climate match!")

        # Check for terrain match using one-hot encoding
        user_terrain = user['preferred_terrain'].values[0]
        terrain_col = f"terrain_{user_terrain}"
        if terrain_col in destination.index and destination[terrain_col] == 1:
            similarity_score += 1
            print("Terrain match!")
        
        # Budget comparison
        if isinstance(destination['avg_daily_budget'], Decimal):
            destination_budget = float(destination['avg_daily_budget'])
        else:
            destination_budget = destination['avg_daily_budget']
        
        if isinstance(user['budget'].values[0], Decimal):
            user_budget = float(user['budget'].values[0])
        else:
            user_budget = user['budget'].values[0]
        
        print(f"Comparing budgets: User's budget {user_budget}, Destination's budget {destination_budget}")
        if abs(destination_budget - user_budget) < 50:
            similarity_score += 1
            print("Budget match!")
        
        return similarity_score

    recommendations = []

    # Loop through the nearest destinations and calculate final score
    for idx in indices[0]:
        destination = destinations_df.iloc[idx]
        # Get KNN-based score (distance)
        knn_score = distances[0][np.where(indices[0] == idx)[0][0]]
        # Calculate similarity score based on user preferences
        similarity_score = calculate_similarity(destination, user)
        # Combine scores
        final_score = (weight_kNN * knn_score) + (weight_similarity * similarity_score)
        
        # Extract country from one-hot encoded columns
        country_columns = [col for col in destination.index if col.startswith('country_')]
        country = [col.split('_')[1] for col in country_columns if destination[col] == 1]
        
        recommendations.append({
            'name': destination['name'],
            'country': ', '.join(country),  # Join the country names if multiple are encoded
            'final_score': final_score,
            'avg_daily_budget': user['budget'].values[0],
            'knn_score': knn_score,
            'similarity_score': similarity_score
        })
    
    recommendations_df = pd.DataFrame(recommendations)
    recommendations_df = recommendations_df.sort_values(by='final_score', ascending=False)

    return recommendations_df[['name', 'country', 'final_score', 'knn_score', 'similarity_score']]

if __name__ == "__main__":
    # Change user id to test different users
    user_id = 7
    recommendations = recommend_destinations(user_id)
    print(recommendations)
