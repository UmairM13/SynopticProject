import pandas as pd
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split
from data_loader import load_processed_data


def prepare_collab_data():
    """Create user-item matrix from past destinations"""
    users_df, destinations_df = load_processed_data()
    
    print("-- Destinations columns:", destinations_df.columns.tolist())
    print("-- Users columns:", users_df.columns.tolist())
    # Clean name columns for case-insensitive matching
    destinations_df['name_clean'] = destinations_df['name'].str.strip().str.lower()

    ratings = []
    for _, user in users_df.iterrows():
        if isinstance(user['past_destinations'], list):
            for dest_name in user['past_destinations']:
                dest_name_clean = dest_name.strip().lower()
                matched_dest = destinations_df[destinations_df['name_clean'] == dest_name_clean]

                if not matched_dest.empty:
                    ratings.append({
                        'user_id': str(user['id']),
                        'destination_id': str(matched_dest['id'].values[0]),
                        'rating': 5  # Implicit feedback (user visited = positive rating)
                    })

    ratings_df = pd.DataFrame(ratings)
    print(f"- Built {len(ratings_df)} user-destination ratings.")
    return ratings_df


def train_collaborative_model():
    ratings_df = prepare_collab_data()

    if ratings_df.empty:
        print("X No ratings available for training.")
        return None

    reader = Reader(rating_scale=(0.5, 5))
    data = Dataset.load_from_df(ratings_df[['user_id', 'destination_id', 'rating']], reader)
    trainset = data.build_full_trainset()

    model = SVD(n_factors=50, n_epochs=20, lr_all=0.005, reg_all=0.02)
    model.fit(trainset)

    print("- Collaborative model trained.")
    return model


def collab_recommendations(user_id, model, n=10):
    users_df, destinations_df = load_processed_data()
    destinations_df['destination_id'] = destinations_df['id'].astype(str)

    # Get destinations the user has already visited
    user_row = users_df[users_df['id'] == int(user_id)]
    visited = user_row.iloc[0]['past_destinations'] if not user_row.empty else []

    visited_lower = [v.lower().strip() for v in visited]
    all_ids = destinations_df[['destination_id', 'name']]

    # Filter out already visited destinations
    unseen = all_ids[~all_ids['name'].str.lower().str.strip().isin(visited_lower)]

    # Predict ratings for unseen destinations
    predictions = []
    for _, row in unseen.iterrows():
        pred = model.predict(str(user_id), row['destination_id'])
        predictions.append((row['destination_id'], pred.est))

    # Top-N recommendations
    top_dest_ids = sorted(predictions, key=lambda x: x[1], reverse=True)[:n]
    recommended_ids = [x[0] for x in top_dest_ids]

    return destinations_df[destinations_df['destination_id'].isin(recommended_ids)][['id', 'name']]


if __name__ == "__main__":
    model = train_collaborative_model()

    if model:
        user_id = 6
        print(f"\nRecommendations for User {user_id}:")
        print(collab_recommendations(user_id, model))
    else:
        print("X No model could be trained.")
