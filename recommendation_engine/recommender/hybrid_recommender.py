import pandas as pd
import numpy as np
from decimal import Decimal
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from datetime import datetime
# from recommendation_engine.recommender.data_loader import load_processed_data
# from recommendation_engine.recommender.content_based_model import prepare_features


from data_loader import load_processed_data
from content_based_model import prepare_features


users_df, destinations_df = load_processed_data()
# Check available columns
# print("Columns in destinations_df:", destinations_df.columns)

current_month = datetime.now().month

# print("\n=== Data Validation ===")
# print("Destination columns:", destinations_df.columns.tolist())
# print("NaN counts:", destinations_df.isna().sum().sum())


# Drop non-numeric columns for model training
drop_columns = ['id', 'name', 'currency']
features = destinations_df.drop(columns=[col for col in drop_columns if col in destinations_df.columns])
# Ensure all columns are numeric
features = features.apply(pd.to_numeric, errors='coerce').fillna(0)
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)
features_scaled = np.nan_to_num(features_scaled, nan=0.0)

# Fit KNN model 
knn = NearestNeighbors(n_neighbors=20, metric='euclidean')
knn.fit(features_scaled)


def compute_past_similarity(destination_name, visited_names, features_df, similarity_matrix): 
    
    if not visited_names or destination_name not in features_df['name'].values:
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


def recommend_destinations(user_id, n_recommendations=10, weight_kNN=0.2, weight_similarity=0.45, weight_past=0.2, weight_off_season=0.15):
    user = users_df[users_df['id'] == user_id]
    if user.empty:
        return "User ID not found in the database."
    
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
    set_one_hot_encoding(user['preferred_climate_original'].values[0], "climate", user_vector)
    set_one_hot_encoding(user['preferred_terrain_original'].values[0], "terrain", user_vector)

    user_vector = pd.DataFrame(user_vector, columns=features.columns)
    user_vector_scaled = scaler.transform(user_vector)
    
    # Find the nearest destinations using KNN (returning n_recommendations neighbors)
    distances, indices = knn.kneighbors(user_vector_scaled, n_neighbors=min(n_recommendations, len(destinations_df)))
    
    # Similarity function based on one-hot encoded columns for climate and terrain and budget comparison
    def calculate_similarity(destination, user):
        def jaccard(set1, set2):
            if not set1 or not set2:
                return 0
            return len(set1 & set2) / len(set1 | set2)
        
        climates = set(map(str.strip, user['preferred_climate_original'].values[0].lower().split(',')))
        terrains = set(map(str.strip, user['preferred_terrain_original'].values[0].lower().split(',')))
        holidays = set(map(str.strip, user['holiday_type_original'].values[0].lower().split(',')))

        dest_climates = {col.split('_', 1)[1].lower() for col in destination.index if col.startswith("climate_") and destination[col] == 1}
        dest_terrains = {col.split('_', 1)[1].lower() for col in destination.index if col.startswith("terrain_") and destination[col] == 1}
        dest_holidays = {col.split('_', 1)[1].lower() for col in destination.index if col.startswith("holiday_type_") and destination[col] == 1}

        climate_score = jaccard(climates, dest_climates)
        terrain_score = jaccard(terrains, dest_terrains)
        holiday_score = jaccard(holidays, dest_holidays)

        user_budget = float(user['budget'].values[0])
        destination_budget = float(destination.get('avg_daily_budget_original', destination['avg_daily_budget']))
        budget_score = 1 if destination_budget <= user_budget else max(0, 1 - (destination_budget - user_budget) / user_budget)

        return (climate_score + terrain_score + holiday_score + budget_score) / 4
    
    recommendations = []
    
    def calculate_off_season_score(destination_row):
        start = destination_row['off_season_start']
        end = destination_row['off_season_end']
        if pd.isna(start) or pd.isna(end):
            return 0.3
        is_off_season = start <= current_month <= end if start <= end else current_month >= start or current_month <= end
        return 1.0 if is_off_season else 0.3
    
    
    # Loop through the nearest destinations and calculate final score
    # Fixed enumerate syntax - needs to be called with an iterable
    for i, idx in enumerate(indices[0]):
        destination = destinations_df.iloc[idx]
        knn_score = distances[0][i]
        similarity_score = calculate_similarity(destination, user)
        content_score = compute_past_similarity(destination['name'], visited, features_df, similarity_matrix)
        normalized_knn_score = 1 / (1 + knn_score)
        normalized_similarity = similarity_score  # already in range [0, 1]
        off_season_score = calculate_off_season_score(destination)

        final_score = (
            weight_kNN * normalized_knn_score +
            weight_similarity * normalized_similarity +
            weight_past * content_score +
            weight_off_season * off_season_score
        )

        country_val = next((col.split('_', 1)[1] for col in destination.index if col.startswith('country_') and destination[col] == 1), 'Unknown')

        recommendations.append({
            'name': destination['name'],
            'country': country_val,
            'final_score': final_score,
            'knn_score': normalized_knn_score,
            'similarity_score': normalized_similarity,
            'content_score': content_score,
            'off_season_score': off_season_score,
            'avg_daily_budget': destination['avg_daily_budget'],
            'is_off_season': "Yes" if off_season_score > 0.5 else "No",
            'id': destination['id']
        })

    recommendations_df = pd.DataFrame(recommendations)
    return recommendations_df.sort_values(by='final_score', ascending=False).head(n_recommendations) if not recommendations_df.empty else "No suitable destinations found."

def explain_recommendation(destination_id, user_id):
    """Provide explanation for a specific destination recommendation in JSON format."""
    user = users_df[users_df['id'] == user_id]
    destination_row = destinations_df[destinations_df['id'] == destination_id]

    if user.empty or destination_row.empty:
        return {"error": "User ID or destination not found."}

    destination = destination_row.iloc[0]
    destination_name = destination['name']
    explanation = {
        "destination": destination_name,
        "match_summary": [],
        "details": {}
    }

    # Jaccard helper
    def jaccard(set1, set2):
        if not set1 or not set2:
            return 0
        return len(set1 & set2) / len(set1 | set2)

    # Prepare sets
    user_climates = set(map(str.lower, map(str.strip, user['preferred_climate_original'].values[0].split(','))))
    user_terrains = set(map(str.lower, map(str.strip, user['preferred_terrain_original'].values[0].split(','))))
    user_holidays = set(map(str.lower, map(str.strip, user['holiday_type_original'].values[0].split(','))))

    dest_climates = set(col.split('_', 1)[1].lower() for col in destination.index if col.startswith("climate_") and destination[col] == 1)
    dest_terrains = set(col.split('_', 1)[1].lower() for col in destination.index if col.startswith("terrain_") and destination[col] == 1)
    dest_holidays = set(col.split('_', 1)[1].lower() for col in destination.index if col.startswith("holiday_type_") and destination[col] == 1)

    # Climate match explanation
    climate_overlap = user_climates & dest_climates
    if climate_overlap:
        explanation["match_summary"].append("climate_match")
    else:
        explanation["details"]["climate_mismatch"] = {
            "user_preference": list(user_climates),
            "destination_climates": list(dest_climates)
        }

    # Terrain match explanation
    terrain_overlap = user_terrains & dest_terrains
    if terrain_overlap:
        explanation["match_summary"].append("terrain_match")
    else:
        explanation["details"]["terrain_mismatch"] = {
            "user_preference": list(user_terrains),
            "destination_terrains": list(dest_terrains)
        }

    # Holiday type match
    holiday_overlap = user_holidays & dest_holidays
    if holiday_overlap:
        explanation["match_summary"].append("holiday_type_match")
    else:
        explanation["details"]["holiday_type_mismatch"] = {
            "user_preference": list(user_holidays),
            "destination_holiday_types": list(dest_holidays)
        }

    # Budget explanation (always include)
    user_budget = float(user['daily_budget'].values[0])
    dest_budget = float(destination.get('avg_daily_budget_original', destination['avg_daily_budget']))
    tolerance = user_budget * 0.1
    within_budget = user_budget + tolerance >= dest_budget

    if within_budget:
        explanation["match_summary"].append("budget_match")

    explanation["details"]["budget"] = {
        "user_daily_budget": round(user_budget, 2),
        "destination_daily_cost": round(dest_budget, 2),
        "within_budget": within_budget
    }
    
    # Off-season explanation
    start = destination['off_season_start']
    end = destination['off_season_end']
    if pd.notna(start) and pd.notna(end):
        import calendar
        month_names = list(calendar.month_name)
        if start <= end:
            off_months = month_names[start:end + 1]
        else:
            off_months = month_names[start:] + month_names[1:end + 1]
        in_off_season = start <= current_month <= end if start <= end else current_month >= start or current_month <= end
        explanation["details"]["off_season"] = {
            "months": off_months,
            "currently_in_off_season": in_off_season
        }

    # Past destination similarity explanation
    from content_based_model import prepare_features
    features_df, similarity_matrix = prepare_features(destinations_df)

    past_destinations = user.iloc[0]['past_destinations']
    visited = []
    if isinstance(past_destinations, (list, np.ndarray, pd.Series)):
        past_destinations = str(past_destinations[0]) if len(past_destinations) > 0 else ""
    if isinstance(past_destinations, str) and past_destinations.strip():
        visited = [d.strip() for d in past_destinations.split(',') if d.strip()]

    similar_to = [
        d for d in visited
        if d in features_df['name'].values and compute_past_similarity(destination_name, [d], features_df, similarity_matrix) > 0.6
    ]
    if similar_to:
        explanation["match_summary"].append("past_similarity")
        explanation["details"]["similar_to_past_destinations"] = similar_to

    return explanation


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
            explanation = explain_recommendation(row['id'], user_id)
            print(explanation)
    else:
        print(recommendations) 