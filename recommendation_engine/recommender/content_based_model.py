import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
# For api
from recommendation_engine.recommender.data_loader import load_processed_data

# For testing
# from data_loader import load_processed_data

def prepare_features(destinations_df):
    drop_columns = ['id', 'name', 'currency'] if 'currency' in destinations_df.columns else ['id', 'name']
    feature_columns = [col for col in destinations_df.columns if col not in drop_columns]
    features = destinations_df[feature_columns].copy()
    features = features.apply(pd.to_numeric, errors='coerce').fillna(0)

    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    similarity_matrix = cosine_similarity(features_scaled)

    features_df = pd.DataFrame(features_scaled, columns=feature_columns)
    features_df['id'] = destinations_df.reset_index(drop=True)['id']
    features_df['name'] = destinations_df.reset_index(drop=True)['name']
    features_df.set_index('id', inplace=True)

    return features_df, similarity_matrix

def recommend_similar_destinations(destination_name, destinations_df, features_df, similarity_matrix, top_n=10):
    destination_name = destination_name.strip().lower()
    destinations_df['name_lower'] = destinations_df['name'].str.strip().str.lower()

    # Check if destination exists
    if destination_name not in destinations_df['name_lower'].values:
        return f"Destination '{destination_name}' not found."

    # Get correct index from destinations_df
    target_row = destinations_df[destinations_df['name_lower'] == destination_name]
    if target_row.empty:
        return f"Destination '{destination_name}' not found."

    target_id = target_row.iloc[0]['id']

    # Get the index position in features_df
    if target_id not in features_df.index:
        return f"Destination ID {target_id} not found in features."

    idx = list(features_df.index).index(target_id)

    sim_scores = list(enumerate(similarity_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = [score for score in sim_scores if score[0] != idx]

    top_matches = sim_scores[:top_n]
    top_ids = [features_df.index[i] for i, _ in top_matches]

    return destinations_df[destinations_df['id'].isin(top_ids)][['id', 'name']]

if __name__ == "__main__":
    _, destinations_df = load_processed_data()
    features_df, similarity_matrix = prepare_features(destinations_df)
    
    input_name = "London"
    recommendations = recommend_similar_destinations(input_name, destinations_df, features_df, similarity_matrix, top_n=10)
    
    print(f"Recommendations for '{input_name}':")
    print(recommendations)
