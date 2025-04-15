import pandas as pd
import numpy as np
from decimal import Decimal
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from recommendation_engine.recommender.data_loader import load_processed_data
from datetime import datetime
from recommendation_engine.recommender.content_based_model import prepare_features


users_df, destinations_df = load_processed_data()
# Check available columns
print("Columns in destinations_df:", destinations_df.columns)

current_month = datetime.now().month


print("\n=== Data Validation ===")
print("Destination columns:", destinations_df.columns.tolist())
print("NaN counts:", destinations_df.isna().sum().sum())


# Drop non-numeric columns for model training
drop_columns = ['id', 'name', 'currency']
features = destinations_df.drop(columns=[col for col in drop_columns if col in destinations_df.columns])

# Ensure all feature columns are numeric
features = features.apply(pd.to_numeric, errors='coerce')

features = features.fillna(0)

# Handle missing values (mean for numerical, mode for categorical)
for col in features.columns:
    if features[col].dtype == 'object':
        features[col] = features[col].fillna(features[col].mode()[0])
    else:
        features[col] = features[col].fillna(features[col].mean())

# Normalize features using StandardScaler
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

print("NaN values before KNN:", np.isnan(features_scaled).sum())
features_scaled = np.nan_to_num(features_scaled, nan=0.0)

# Fit the KNN model with increased neighbors (set to 20)
n_neighbors = 20
knn = NearestNeighbors(n_neighbors=n_neighbors, metric='euclidean')
knn.fit(features_scaled)


def compute_past_similarity(destination_name, visited_names, features_df, similarity_matrix): 
    
    if not visited_names:
        return 0.0
    
    if destination_name not in features_df['name'].values:
        return 0.0
    
    target_id = features_df[features_df['name'] == destination_name].index[0]
    idx = list(features_df.index).index(target_id)
    
    scores = []
    for past in visited_names:
        if past in features_df['name'].values:
            past_id = features_df[features_df['name'] == past].index[0]
            past_idx = list(features_df.index).index(past_id)
            scores.append(similarity_matrix[idx][past_idx])
            
    
    return np.mean(scores) if scores else 0.0


def recommend_destinations(user_id, n_recommendations=10, weight_kNN=0.5, weight_similarity=0.3, weight_past=0.2):
    user = users_df[users_df['id'] == user_id]
    if user.empty:
        return "User ID not found in the database."
    
    print("HEHREREHREHREHRHHERHERHERHHRh")
    print(users_df.columns.tolist())
    
    features_df, similarity_matrix = prepare_features(destinations_df)
    
    # Get user's past destinations safely
    past_destinations = user.iloc[0]['past_destinations'] if 'past_destinations' in user.columns else None

    # If it's a list/array/Series, flatten it to a string
    if isinstance(past_destinations, (list, np.ndarray, pd.Series)):
        past_destinations = str(past_destinations[0]) if len(past_destinations) > 0 else ""

    # Now safely split
    if isinstance(past_destinations, str) and past_destinations.strip():
        visited = [d.strip() for d in past_destinations.split(',') if d.strip()]
    else:
        visited = []
        
        
    # Initialize user vector with zeros based on features
    user_vector = pd.DataFrame(0, index=[0], columns=features.columns)
    # Set budget
    user_vector['avg_daily_budget'] = user['budget'].values[0]
    
    # Function to set one-hot encoding based on user preference
    def set_one_hot_encoding(preference, column_prefix, user_vector):
        if pd.notna(preference):
            column_name = f"{column_prefix}_{preference}"
            if column_name in user_vector.columns:
                user_vector[column_name] = 1

    # One-hot encoding for nationality, climate, and terrain preferences
    set_one_hot_encoding(user['nationality'].values[0], "country", user_vector)
    set_one_hot_encoding(user['preferred_climate'].values[0], "climate", user_vector)
    set_one_hot_encoding(user['preferred_terrain'].values[0], "terrain", user_vector)

    user_vector = pd.DataFrame(user_vector, columns=features.columns)
    user_vector_scaled = scaler.transform(user_vector)
    
    # Find the nearest destinations using KNN (returning n_recommendations neighbors)
    distances, indices = knn.kneighbors(user_vector_scaled, n_neighbors=min(n_recommendations, len(destinations_df)))
    
    # Similarity function based on one-hot encoded columns for climate and terrain and budget comparison
    def calculate_similarity(destination, user):
        similarity_score = 0

        # Compare climate using one-hot encoded column names.
        user_climate = user['preferred_climate'].values[0]
        climate_col = f"climate_{user_climate}"
        if climate_col in destination.index and destination[climate_col] == 1:
            similarity_score += 1
            print("Climate match!")
        else:
            print(f"No match for climate: expected {climate_col}")

        # Compare terrain using one-hot encoded column names.
        user_terrain = user['preferred_terrain'].values[0]
        terrain_col = f"terrain_{user_terrain}"
        if terrain_col in destination.index and destination[terrain_col] == 1:
            similarity_score += 1
            print("Terrain match!")
        else:
            print(f"No match for terrain: expected {terrain_col}")

        # Budget comparison (within $50 range)
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
    
    def calculate_off_season_score(destination_row):
        current_month = datetime.now().month
        start = destination_row['off_season_start']
        end = destination_row['off_season_end']
        
        if pd.isna(start) or pd.isna(end):
            return 0.3
        if start <= end:
            is_off_season = start <= current_month <= end
        else:
            is_off_season = current_month >= start or current_month <= end
        
        return 1.0 if is_off_season else 0.3
    
    
    # Loop through the nearest destinations and calculate final score
    # Fixed enumerate syntax - needs to be called with an iterable
    for i, idx in enumerate(indices[0]):
        destination = destinations_df.iloc[idx]
        knn_score = distances[0][i]  # Use i directly since we're enumerating
        similarity_score = calculate_similarity(destination, user)
        content_score = compute_past_similarity(destination['name'], visited, features_df, similarity_matrix)
        
        # Normalize scores for weighted calculation
        normalized_knn_score = 1 / (1 + knn_score)  # Transform distance to similarity (closer to 1 means more similar)
        normalized_similarity = similarity_score / 3.0  # Max similarity is 3 (climate, terrain, budget)
        
        final_score = (
            weight_kNN * normalized_knn_score +
            weight_similarity * normalized_similarity +
            weight_past * content_score
        )
        
        off_season_score = calculate_off_season_score(destination)
        
        # Extract country value more safely
        country_val = 'Unknown'
        country_columns = [col for col in destination.index if col.startswith('country_')]
        for col in country_columns:
            if destination[col] == 1:
                country_val = col.split('_', 1)[1]
                break
        
        recommendations.append({
            'name': destination['name'],
            'country': country_val,
            'final_score': final_score,
            'knn_score': normalized_knn_score,
            'similarity_score': normalized_similarity,
            'content_score': content_score,
            'off_season_score': off_season_score,
            'avg_daily_budget': destination['avg_daily_budget'],
            'is_off_season': "Yes" if off_season_score > 0.5 else "No"
        })
    
    recommendations_df = pd.DataFrame(recommendations)
    if recommendations_df.empty:
        return "No suitable destinations found."
        
    recommendations_df = recommendations_df.sort_values(by='final_score', ascending=False)
    
    # Return top n recommendations
    return recommendations_df.head(n_recommendations)

def explain_recommendation(destination_name, user_id):
    """Provide explanation for a specific destination recommendation."""
    
    user = users_df[users_df['id'] == user_id]
    destination = destinations_df[destinations_df['name'] == destination_name]
    
    if user.empty or destination.empty:
        return "User ID or destination not found."
    
    destination = destination.iloc[0]
    explanation = [f"Why {destination_name} is recommended:"]
    
    
    # Check if climate match
    if 'preferred_climate' in user.columns:
        user_climate = user['preferred_climate'].values[0]
        climate_col = f"climate_{user_climate}"
        if climate_col in destination.index and destination[climate_col] == 1:
            explanation.append(f"- The {user_climate} climate matches your preferred climate.")
        else:
            actual_climates = [col.split('_')[1] for col in destination.index if col.startswith("climate_") and destination[col] == 1]  
            if actual_climates:
                explanation.append(f"x Climate differs: {destination_name} has {', '.join(actual_climates)} climate.")
                
    
    # Check if terrain match
    if 'preferred_terrain' in user.columns:
        user_terrain = user['preferred_terrain'].values[0]
        terrain_col = f"terrain_{user_terrain}"
        if terrain_col in destination.index and destination[terrain_col] == 1:
            explanation.append(f"- The {user_terrain} terrain matches your preferred terrain.")
        else:
            actual_terrains = [col.split('_')[1] for col in destination.index if col.startswith("terrain_") and destination[col] == 1]  
            if actual_terrains:
                explanation.append(f"x Terrain differs: {destination_name} has {', '.join(actual_terrains)} terrain.")
    
    # Check budget compatibility
    if 'budget' in user.columns and 'avg_daily_budget' in destination.index:
        user_budget = float(user['budget'].values[0]) if isinstance(user['budget'].values[0], Decimal) else user['budget'].values[0]
        destination_budget = float(destination['avg_daily_budget']) if isinstance(destination['avg_daily_budget'], Decimal) else destination['avg_daily_budget']
        
        if abs(destination_budget - user_budget) < 50:
            explanation.append(f"- The average daily budget of {destination_name} is within your budget.")
        else:
            explanation.append(f"x Budget differs: {destination_name} has an average daily budget of {destination_budget}.")
            
            
    # Check off-season preference
    if 'off_season_start' in destination.index and 'off_season_end' in destination.index:
        if pd.notna(destination['off_season_start']) and pd.notna(destination['off_season_end']):
            off_start = int(destination['off_season_start'])
            off_end = int(destination['off_season_end'])
            
            # Get month names
            import calendar
            month_names = list(calendar.month_name)
            off_season_months = []
            
            if off_start <= off_end:
                off_season_months = month_names[off_start:off_end+1]
            else:
                off_season_months = month_names[off_start:] + month_names[1:off_end+1]
            
            if current_month >= off_start or current_month <= off_end:
                explanation.append(f"✓ Off-season bonus: Currently in off-season ({', '.join(off_season_months)})")
            else:
                explanation.append(f"× Note: Off-season is {', '.join(off_season_months)}")
    
    # Content-based similarity explanation 
    features_df, similarity_matrix = prepare_features(destinations_df)
    
    if 'past_destinations' in user.columns:
        past_destinations = user.iloc[0]['past_destinations']
        
        if isinstance(past_destinations, (list, np.ndarray, pd.Series)):
                past_destinations = str(past_destinations[0]) if len(past_destinations) > 0 else ""

        if isinstance(past_destinations, str) and past_destinations.strip():
                visited = [d.strip() for d in past_destinations.split(',') if d.strip()]
        else:
            visited = []
    else:
        visited = []  
    
    similar_to = [d for d in visited if d in features_df['name'].values and compute_past_similarity(destination_name, [d], features_df, similarity_matrix) > 0.6]    
    if similar_to:
        explanation.append(f"- Similar to your past destinations: {', '.join(similar_to)}")
        
    return "\n".join(explanation)

if __name__ == "__main__":
    # Test with users
    user_id = 6
    print(f"Generating recommendations for user {user_id}")
    recommendations = recommend_destinations(user_id)
    
    if isinstance(recommendations, pd.DataFrame) and not recommendations.empty:
        print("\nTop Recommendations:")
        print(recommendations[['name', 'country', 'is_off_season']])
        
        # Generate explanations for each recommended destination
        print("\nExplanation Details:")
        for _, row in recommendations.iterrows():
            print("\n" + "="*50)
            explanation = explain_recommendation(row['name'], user_id)
            print(explanation)
    else:
        print(recommendations) 