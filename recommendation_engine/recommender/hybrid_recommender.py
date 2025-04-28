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

# Initialize data
current_month = datetime.now().month

# Load data
data_manager = DataManager.get_instance()
users_df = data_manager.get_users()
destinations_df = data_manager.get_destinations()
past_destinations_df = data_manager.get_past_destinations()

# Prepare features
irrelevant_columns = [
    'IATA_code', 'departure_city', 'departure_country', 'destination_id',
    'user_id', 'name', 'flight_cost', 'flight_cost_original',
    'hotel_cost', 'hotel_cost_original', 'train_cost',
    'avg_daily_budget_original'
] + [col for col in destinations_df.columns if col.startswith('language_')]

features_for_knn = destinations_df.drop(columns=irrelevant_columns, errors='ignore')
features_for_knn = features_for_knn.select_dtypes(include=['number'])
# Only scale avg_daily_budget
scaler_budget = StandardScaler()
if 'avg_daily_budget' in features_for_knn.columns:
    features_for_knn['avg_daily_budget'] = scaler_budget.fit_transform(features_for_knn[['avg_daily_budget']])

# KNN Model
knn = NearestNeighbors(n_neighbors=20, metric='cosine')
knn.fit(features_for_knn)

# Content model
features_df, similarity_matrix = prepare_features(destinations_df)



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


def recommend_destinations(user_id, users_df, destinations_df, past_destinations_df, n_recommendations=20, weight_kNN=0.24, weight_similarity=0.45, weight_past=0.26, weight_off_season=0.05):
    user = users_df[users_df['id'] == user_id]
    if user.empty:
        return "User not found"

    user_vector = pd.DataFrame(0, index=[0], columns=features_for_knn.columns)

    if 'avg_daily_budget' in user_vector.columns:
        user_vector['avg_daily_budget'] = scaler_budget.transform([[user['budget'].values[0]]])[0][0]

    def set_one_hot(preference, prefix):
        if pd.notna(preference):
            prefs = str(preference).split(',')
            for pref in prefs:
                col = f"{prefix}_{pref.strip().lower()}"
                if col in user_vector.columns:
                    user_vector.at[0, col] = 1

    set_one_hot(user['nationality'].values[0], 'country')
    set_one_hot(user['preferred_climate_original'].values[0], 'climate')
    set_one_hot(user['preferred_terrain_original'].values[0], 'terrain')
    set_one_hot(user['holiday_type_original'].values[0], 'holiday_type')

    distances, indices = knn.kneighbors(user_vector, n_neighbors=min(n_recommendations, len(destinations_df)))
    max_distance = distances.max()
    
    recommendations = []

    for i, idx in enumerate(indices[0]):
        destination = destinations_df.iloc[idx]

        if max_distance == 0:
            normalized_knn_score = 1.0
        else:
            normalized_knn_score = 1 - distances[0][i]
            normalized_knn_score = max(0, normalized_knn_score)
        
        # Similarity calculation
        def jaccard(set1, set2):
            if not set1: return 1
            if not set2: return 0
            return len(set1 & set2) / len(set1 | set2)

        def get_set(destination, prefix):
            return {col.split('_', 1)[1].lower() for col in destination.index if col.startswith(prefix) and destination[col] == 1}

        climates = set(map(str.strip, user['preferred_climate_original'].values[0].lower().split(','))) if 'any' not in user['preferred_climate_original'].values[0].lower() else set()
        terrains = set(map(str.strip, user['preferred_terrain_original'].values[0].lower().split(','))) if 'any' not in user['preferred_terrain_original'].values[0].lower() else set()
        holidays = set(map(str.strip, user['holiday_type_original'].values[0].lower().split(','))) if 'any' not in user['holiday_type_original'].values[0].lower() else set()

        dest_climates = get_set(destination, 'climate')
        dest_terrains = get_set(destination, 'terrain')
        dest_holidays = get_set(destination, 'holiday_type')

        climate_score = jaccard(climates, dest_climates)
        terrain_score = jaccard(terrains, dest_terrains)
        holiday_score = jaccard(holidays, dest_holidays)

        user_budget = float(user['budget'].values[0])
        dest_budget = destination.get('avg_daily_budget_original', destination['avg_daily_budget'])
        budget_score = 1 if dest_budget <= user_budget else max(0, 1 - (dest_budget - user_budget) / user_budget)

        similarity_score = (climate_score + terrain_score + holiday_score + budget_score) / 4

        # Past travel similarity
        destination_name = destination['name']
        past_similarity = compute_past_similarity(destination_name, user_id, features_df, similarity_matrix, past_destinations_df)
        
        # Squash past similarity to [0, 1]
        past_similarity = past_similarity / (1 + past_similarity)
        
        # Off season
        start = destination['off_season_start']
        end = destination['off_season_end']
        off_season_score = 0.5
        if pd.notna(start) and pd.notna(end):
            if start <= end:
                off_season = start <= current_month <= end
            else:
                off_season = current_month >= start or current_month <= end
            off_season_score = 0.65 if off_season else 0.5

        final_score = (
            weight_kNN * normalized_knn_score +
            weight_similarity * similarity_score +
            weight_past * past_similarity +
            weight_off_season * off_season_score
        )

        country_val = next((col.split('_', 1)[1] for col in destination.index if col.startswith('country_') and destination[col] == 1), 'Unknown')

        recommendations.append({
            'id': destination['id'],
            'name': destination['name'],
            'country': country_val,
            'final_score': final_score,
            'knn_score': normalized_knn_score,
            'similarity_score': similarity_score,
            'past_similarity': past_similarity,
            'off_season_score': off_season_score,
            'avg_daily_budget': dest_budget,
            'is_off_season': 'Yes' if off_season_score > 0.58 else 'No'
        })

    recommendations_df = pd.DataFrame(recommendations)
    return recommendations_df.sort_values('final_score', ascending=False).head(n_recommendations)

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
                           weight_kNN=0.24, 
                           weight_similarity=0.45, 
                           weight_past=0.26, 
                           weight_off_season=0.05):
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
    user_climates = set(map(str.strip, climate_raw.split(','))) if "any" not in climate_raw else set()
    climate_display = list(user_climates) if user_climates else ["any (matches all)"]

    terrain_raw = user['preferred_terrain_original'].values[0].lower()
    user_terrains = set(map(str.strip, terrain_raw.split(','))) if "any" not in terrain_raw else set()
    terrain_display = list(user_terrains) if user_terrains else ["any (matches all)"]

    holidays_raw = user['holiday_type_original'].values[0].lower()
    user_holidays = set(map(str.strip, holidays_raw.split(','))) if "any" not in holidays_raw else set()
    holiday_display = list(user_holidays) if user_holidays else ["any (matches all)"]

    dest_climates = {col.split('_', 1)[1].lower() for col in destination.index if col.startswith("climate_") and destination[col] == 1}
    dest_terrains = {col.split('_', 1)[1].lower() for col in destination.index if col.startswith("terrain_") and destination[col] == 1}
    dest_holidays = {col.replace("holiday_type_", "").strip().lower() for col in destination.index if col.startswith("holiday_type_") and destination[col] == 1}

    # Helper: Jaccard similarity
    def jaccard(set1, set2):
        if not set1:
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

    # Prepare the real features for KNN match (cosine distance)
    irrelevant_columns = [
        'IATA_code', 'departure_city', 'departure_country', 'destination_id',
        'user_id', 'name', 'flight_cost', 'flight_cost_original',
        'hotel_cost', 'hotel_cost_original', 'train_cost',
        'avg_daily_budget_original'
    ] + [col for col in destinations_df.columns if col.startswith('language_')]

    features_for_knn = destinations_df.drop(columns=irrelevant_columns, errors='ignore')
    features_for_knn = features_for_knn.select_dtypes(include=['number'])

    scaler_budget = StandardScaler()
    if 'avg_daily_budget' in features_for_knn.columns:
        features_for_knn['avg_daily_budget'] = scaler_budget.fit_transform(features_for_knn[['avg_daily_budget']])

    knn_model = NearestNeighbors(n_neighbors=20, metric='cosine')
    knn_model.fit(features_for_knn)

    # Build user vector
    user_vector = pd.DataFrame(0, index=[0], columns=features_for_knn.columns)
    if 'avg_daily_budget' in user_vector.columns:
        user_vector['avg_daily_budget'] = scaler_budget.transform([[user_budget]])[0][0]

    for climate in user_climates:
        col = f"climate_{climate}"
        if col in user_vector.columns:
            user_vector[col] = 1
    for terrain in user_terrains:
        col = f"terrain_{terrain}"
        if col in user_vector.columns:
            user_vector[col] = 1
    for holiday in user_holidays:
        col = f"holiday_type_{holiday}"
        if col in user_vector.columns:
            user_vector[col] = 1
    nationality_col = f"country_{user['nationality'].values[0].strip().lower()}"
    if nationality_col in user_vector.columns:
        user_vector[nationality_col] = 1

    distances, indices = knn_model.kneighbors(user_vector, n_neighbors=len(destinations_df))
    destination_idx = destinations_df[destinations_df['id'] == destination_id].index[0]
    knn_distance = distances[0][list(indices[0]).index(destination_idx)]
    normalized_knn_score = 1 - knn_distance
    normalized_knn_score = max(0, normalized_knn_score)

    # Past destination similarity (content score)
    features_df, similarity_matrix = prepare_features(destinations_df)
    content_score = compute_past_similarity(destination['name'], user_id, features_df, similarity_matrix, past_destinations_df)
    content_score = content_score / (1 + content_score)  # squash

    # Match score using preference similarity
    preference_similarity = (
        jaccard(user_climates, dest_climates) +
        jaccard(user_terrains, dest_terrains) +
        jaccard(user_holidays, dest_holidays) +
        (1 if within_budget else max(0, 1 - (dest_budget - user_budget) / user_budget))
    ) / 4

    # Off-season score
    start = destination['off_season_start']
    end = destination['off_season_end']
    off_season_score = 0.5
    if pd.notna(start) and pd.notna(end):
        if start <= end:
            in_off_season = start <= current_month <= end
            months_from_season = min(abs(current_month - start), abs(current_month - end))
        else:
            in_off_season = current_month >= start or current_month <= end
            months_from_season = min((current_month - start) % 12, (end - current_month) % 12)

        if in_off_season:
            off_season_score = 0.6
        else:
            off_season_score = 0.5 + max(0, 0.1 - (months_from_season * 0.02))

    explanation["details"]["off_season"] = {
        "currently_in_off_season": bool(in_off_season),
        "score": round(off_season_score, 3)
    }

    # Final weighted score
    final_score = (
        weight_kNN * normalized_knn_score +
        weight_similarity * preference_similarity +
        weight_past * content_score +
        weight_off_season * off_season_score
    )

    explanation["details"]["score_breakdown"] = {
        "final_score": round(final_score, 3),
        "knn_score": round(normalized_knn_score, 3),
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