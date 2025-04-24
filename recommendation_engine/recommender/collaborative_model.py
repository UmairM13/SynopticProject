import pandas as pd
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split
from recommendation_engine.recommender.data_loader import load_processed_data


def prepare_collab_data():
    """Creates a user-item interaction matrix using the structured past_destinations table."""
    users_df, destinations_df, past_destinations_df = load_processed_data()

    # Clean up IDs and destination names
    past_destinations_df["destination_name_clean"] = past_destinations_df["destination_name"].str.lower().str.strip()
    destinations_df["name_clean"] = destinations_df["name"].str.lower().str.strip()

    # Merge past destinations with valid destination IDs
    merged = past_destinations_df.merge(
        destinations_df[["id", "name_clean"]],
        left_on="destination_name_clean",
        right_on="name_clean",
        how="inner"
    )

    if merged.empty:
        print("X No matched past destinations.")
        return pd.DataFrame()

    ratings_df = merged[["user_id", "id"]].copy()
    ratings_df.rename(columns={"id": "destination_id"}, inplace=True)
    ratings_df["user_id"] = ratings_df["user_id"].astype(str)
    ratings_df["destination_id"] = ratings_df["destination_id"].astype(str)
    ratings_df["rating"] = 5  # Implicit: visited = liked

    print(f"- Built {len(ratings_df)} interactions from past_destinations.")
    return ratings_df


def train_collaborative_model():
    ratings_df = prepare_collab_data()
    if ratings_df.empty:
        print("X No data available for training.")
        return None

    reader = Reader(rating_scale=(0.5, 5))
    data = Dataset.load_from_df(ratings_df[["user_id", "destination_id", "rating"]], reader)
    trainset = data.build_full_trainset()

    model = SVD(n_factors=50, n_epochs=20, lr_all=0.005, reg_all=0.02)
    model.fit(trainset)

    print("- Collaborative model trained.")
    return model


def collab_recommendations(user_id, model, n=10):
    users_df, destinations_df, past_destinations_df = load_processed_data()
    destinations_df["destination_id"] = destinations_df["id"].astype(str)

    visited_ids = past_destinations_df[past_destinations_df["user_id"] == user_id]["destination_name"].str.lower().str.strip()
    visited_ids = destinations_df[destinations_df["name"].str.lower().str.strip().isin(visited_ids)]["destination_id"].tolist()

    # Filter unseen destinations
    unseen_df = destinations_df[~destinations_df["destination_id"].isin(visited_ids)]

    # Predict and rank
    predictions = []
    for _, row in unseen_df.iterrows():
        pred = model.predict(str(user_id), row["destination_id"])
        predictions.append((row["id"], row["name"], pred.est))

    top_predictions = sorted(predictions, key=lambda x: x[2], reverse=True)[:n]
    top_df = pd.DataFrame(top_predictions, columns=["id", "name", "predicted_rating"])

    return top_df


if __name__ == "__main__":
    model = train_collaborative_model()
    if model:
        user_id = 6
        print(f"\nCollaborative Recommendations for User {user_id}:")
        print(collab_recommendations(user_id, model))
    else:
        print("X No model could be trained.")
