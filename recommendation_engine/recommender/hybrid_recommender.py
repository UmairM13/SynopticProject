import pandas as pd
import numpy as np
import calendar
from decimal import Decimal
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from datetime import datetime
# For api
from recommendation_engine.recommender.data_loader import DataManager
from recommendation_engine.recommender.content_based_model import prepare_features

# For testing 
# from data_loader import load_processed_data
# from content_based_model import prepare_features


users_df, destinations_df, past_destinations_df = DataManager.refresh()
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


def compute_past_similarity(destination_name, user_id, features_df, similarity_matrix, past_destinations_df):
    now = pd.Timestamp.now()
    destination_name = destination_name.strip().lower()
    features_df = features_df.copy()
    features_df["name_lower"] = features_df["name"].str.lower().str.strip()

    if destination_name not in features_df["name_lower"].values:
        return 0.0

    user_history = past_destinations_df[past_destinations_df["user_id"] == user_id]
    if user_history.empty:
        return 0.0

    target_index = features_df[features_df["name_lower"] == destination_name].index[0]
    target_pos = features_df.index.get_loc(target_index)
    scores = []
    weights = []

    for _, row in user_history.iterrows():
        past_name = row["destination_name"].strip().lower()
        trip_end = pd.to_datetime(row["trip_end_date"], errors="coerce")
        if past_name in features_df["name_lower"].values and pd.notna(trip_end):
            past_index = features_df[features_df["name_lower"] == past_name].index[0]
            past_pos = features_df.index.get_loc(past_index)
            distance = similarity_matrix[target_pos][past_pos]
            similarity = 1 / (1 + distance)

            months_ago = max(1, (now.year - trip_end.year) * 12 + now.month - trip_end.month)
            weight = 1 / months_ago

            scores.append(similarity * weight)
            weights.append(weight)

    return np.sum(scores) / np.sum(weights) if weights else 0.0


def recommend_destinations(user_id, n_recommendations=10, weight_kNN=0.2, weight_similarity=0.35, weight_past=0.2, weight_off_season=0.25):
    user = users_df[users_df['id'] == user_id]
    if user.empty:
        return "User ID not found in the database."
    
    features_df, similarity_matrix = prepare_features(destinations_df) 
        
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
    for climate in user['preferred_climate_original'].values[0].split(','):
        set_one_hot_encoding(climate.strip(), "climate", user_vector)
    for terrain in user['preferred_terrain_original'].values[0].split(','):
        set_one_hot_encoding(terrain.strip(), "terrain", user_vector)

    user_vector = pd.DataFrame(user_vector, columns=features.columns)
    user_vector_scaled = scaler.transform(user_vector)
    
    # Find the nearest destinations using KNN (returning n_recommendations neighbors)
    distances, indices = knn.kneighbors(user_vector_scaled, n_neighbors=min(n_recommendations, len(destinations_df)))
    
    # Similarity function based on one-hot encoded columns for climate and terrain and budget comparison
    def calculate_similarity(destination, user):
        def jaccard(set1, set2):
            if not set1:  # If preference was 'any'
                return 1
            if not set2:
                return 0
            return len(set1 & set2) / len(set1 | set2)
        
        climates_raw = user['preferred_climate_original'].values[0].lower()
        climates = set() if "any" in climates_raw else set(map(str.strip, climates_raw.split(',')))

        terrains_raw = user['preferred_terrain_original'].values[0].lower()
        terrains = set() if "any" in terrains_raw else set(map(str.strip, terrains_raw.split(',')))

        holidays_raw = user['holiday_type_original'].values[0].lower()
        holidays = set() if "any" in holidays_raw else set(map(str.strip, holidays_raw.split(',')))

        dest_climates = {col.split('_', 1)[1].lower() for col in destination.index if col.startswith("climate_") and destination[col] == 1}
        dest_terrains = {col.split('_', 1)[1].lower() for col in destination.index if col.startswith("terrain_") and destination[col] == 1}
        dest_holidays = set(col.replace("holiday_type_", "").strip().lower() for col in destination.index if col.startswith("holiday_type_") and destination[col] == 1)

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
        content_score = compute_past_similarity(destination['name'], user_id, features_df, similarity_matrix, past_destinations_df)
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
            'avg_daily_budget': destination['avg_daily_budget_original'],
            'is_off_season': "Yes" if off_season_score > 0.5 else "No",
            'id': destination['id']
        })

    recommendations_df = pd.DataFrame(recommendations)
    return recommendations_df.sort_values(by='final_score', ascending=False).head(n_recommendations) if not recommendations_df.empty else "No suitable destinations found."


def convert_numpy_types(obj):
    if isinstance(obj, (np.bool_, np.bool8)):
        return bool(obj)
    elif isinstance(obj, (np.integer,)):
        return int(obj)
    elif isinstance(obj, (np.floating,)):
        return float(obj)
    elif isinstance(obj, (np.ndarray,)):
        return obj.tolist()
    return obj


def clean_explanation(explanation):
    if isinstance(explanation, dict):
        return {k: clean_explanation(v) for k, v in explanation.items()}
    elif isinstance(explanation, list):
        return [clean_explanation(i) for i in explanation]
    else:
        return convert_numpy_types(explanation)
    
    
def explain_recommendation(destination_id, user_id, 
                           weight_kNN=0.2, 
                           weight_similarity=0.35, 
                           weight_past=0.2, 
                           weight_off_season=0.25):
    """Provide enhanced explanation for a specific destination recommendation."""
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

    # Setup sets for preference comparison
    climate_raw = user['preferred_climate_original'].values[0].lower()
    if "any" in climate_raw:
        user_climates = set()
        climate_display = ["any (matches all)"]
    else:
        user_climates = set(map(str.strip, climate_raw.split(',')))
        climate_display = list(user_climates)
    
    terrain_raw = user['preferred_terrain_original'].values[0].lower()
    if "any" in terrain_raw:
        user_terrains = set()
        terrain_display = ["any (matches all)"]
    else:
        user_terrains = set(map(str.strip, terrain_raw.split(',')))
        terrain_display = list(user_terrains)

    holidays_raw = user['holiday_type_original'].values[0].lower()
    if "any" in holidays_raw:
        user_holidays = set()
        holiday_display = ["any (matches all)"]
    else:
        user_holidays = set(map(str.strip, holidays_raw.split(',')))
        holiday_display = list(user_holidays)
        
    dest_climates = {col.split('_', 1)[1].lower() for col in destination.index if col.startswith("climate_") and destination[col] == 1}
    dest_terrains = {col.split('_', 1)[1].lower() for col in destination.index if col.startswith("terrain_") and destination[col] == 1}
    dest_holidays = {col.replace("holiday_type_", "").strip().lower() for col in destination.index if col.startswith("holiday_type_") and destination[col] == 1}

    # Helper: Jaccard similarity
    def jaccard(set1, set2):
        if not set1:  # If preference was 'any'
            return 1
        if not set2:
            return 0
        return len(set1 & set2) / len(set1 | set2)

    # Climate
    climate_overlap = user_climates & dest_climates
    explanation["details"]["climate"] = {
        "user_preference": climate_display,
        "destination_climates": list(dest_climates),
        "matches": list(climate_overlap),
        "mismatches": list(user_climates - climate_overlap) if user_climates else []
    }
    if climate_overlap:
        explanation["match_summary"].append("climate_match")

    # Terrain
    terrain_overlap = user_terrains & dest_terrains
    explanation["details"]["terrain"] = {
        "user_preference": terrain_display,
        "destination_terrains": list(dest_terrains),
        "matches": list(terrain_overlap),
        "mismatches": list(user_terrains - terrain_overlap) if user_terrains else []
    }
    if terrain_overlap:
        explanation["match_summary"].append("terrain_match")

    # Holiday type
    holiday_overlap = user_holidays & dest_holidays
    explanation["details"]["holiday_type"] = {
        "user_preference": holiday_display,
        "destination_holiday_types": list(dest_holidays),
        "matches": list(holiday_overlap),
        "mismatches": list(user_holidays - holiday_overlap) if user_holidays else []
    }
    if holiday_overlap:
        explanation["match_summary"].append("holiday_type_match")

    # Budget match
    user_budget = float(user['daily_budget'].values[0])
    dest_budget = float(destination.get('avg_daily_budget_original', destination['avg_daily_budget']))
    budget_gap = user_budget - dest_budget
    tolerance = user_budget * 0.1
    within_budget = user_budget + tolerance >= dest_budget

    explanation["details"]["budget"] = {
        "user_daily_budget": round(user_budget, 2),
        "destination_daily_cost": round(dest_budget, 2),
        "budget_gap": round(budget_gap, 2),
        "within_budget": bool(within_budget)
    }

    if within_budget:
        explanation["match_summary"].append("budget_match")

    # Off-season check
    start = destination['off_season_start']
    end = destination['off_season_end']
    in_off_season = False
    if pd.notna(start) and pd.notna(end):
        month_names = list(calendar.month_name)
        if start <= end:
            off_months = month_names[start:end + 1]
        else:
            off_months = month_names[start:] + month_names[1:end + 1]
        in_off_season = start <= current_month <= end if start <= end else current_month >= start or current_month <= end
        explanation["details"]["off_season"] = {
            "months": off_months,
            "currently_in_off_season": bool(in_off_season)
        }

    # Past destination similarity score
    features_df, similarity_matrix = prepare_features(destinations_df)
    
    content_score = compute_past_similarity(destination['name'], user_id, features_df, similarity_matrix, past_destinations_df)

    # kNN Score (recompute distance from user vector)
    drop_columns = ['id', 'name', 'currency']
    features = destinations_df.drop(columns=[col for col in drop_columns if col in destinations_df.columns])
    features = features.apply(pd.to_numeric, errors='coerce').fillna(0)
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    knn_model = NearestNeighbors(n_neighbors=20, metric='euclidean')
    knn_model.fit(features_scaled)

    user_vector = pd.DataFrame(0, index=[0], columns=features.columns)
    user_vector['avg_daily_budget'] = user_budget
    for climate in user_climates:
        col = f"climate_{climate}"
        if col in user_vector.columns:
            user_vector[col] = 1
    for terrain in user_terrains:
        col = f"terrain_{terrain}"
        if col in user_vector.columns:
            user_vector[col] = 1
    nationality_col = f"country_{user['nationality'].values[0]}"
    if nationality_col in user_vector.columns:
        user_vector[nationality_col] = 1

    user_vector_scaled = scaler.transform(user_vector)
    distances, indices = knn_model.kneighbors(user_vector_scaled, n_neighbors=len(destinations_df))
    destination_idx = destinations_df[destinations_df['id'] == destination_id].index[0]
    knn_distance = distances[0][list(indices[0]).index(destination_idx)]
    knn_score = 1 / (1 + knn_distance)

    # Match score using preference similarity
    preference_similarity = (
        jaccard(user_climates, dest_climates) +
        jaccard(user_terrains, dest_terrains) +
        jaccard(user_holidays, dest_holidays) +
        (1 if within_budget else max(0, 1 - (dest_budget - user_budget) / user_budget))
    ) / 4

    # Off-season score
    off_season_score = 1.0 if in_off_season else 0.3

    # Final weighted score
    final_score = (
        weight_kNN * knn_score +
        weight_similarity * preference_similarity +
        weight_past * content_score +
        weight_off_season * off_season_score
    )

    # Score breakdown
    explanation["details"]["score_breakdown"] = {
        "final_score": round(final_score, 3),
        "knn_score": round(knn_score, 3),
        "preference_similarity": round(preference_similarity, 3),
        "past_destination_similarity": round(content_score, 3),
        "off_season_score": round(off_season_score, 3),
        "weights": {
            "kNN": weight_kNN,
            "similarity": weight_similarity,
            "past": weight_past,
            "off_season": weight_off_season
        }
    }

    # Similar destinations
    destination_name_clean = str(destination_name).strip().lower()
    if destination_name_clean in features_df['name'].str.lower().values:
        dest_idx = features_df[features_df['name'].str.lower() == destination_name_clean].index[0]
        similarities = similarity_matrix[dest_idx]
        sorted_indices = np.argsort(similarities)[::-1]
        top_matches = []
        for idx in sorted_indices:
            if idx == dest_idx:
                continue
            match_name = features_df.iloc[idx]['name']
            top_matches.append({
                "name": match_name,
                "similarity_score": round(float(similarities[idx]), 3)
            })
            if len(top_matches) >= 3:
                break
        explanation["details"]["similar_destinations"] = top_matches
        explanation["match_summary"].append("has_similar_destinations")

    return clean_explanation(explanation)



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