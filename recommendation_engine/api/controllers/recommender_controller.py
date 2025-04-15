from recommendation_engine.recommender.hybrid_recommender import recommend_destinations as hybrid_recommend, explain_recommendation
import os
import subprocess


def get_recommendations_for_user(user_id: int):
    return hybrid_recommend(user_id)

def get_explanation_for_destination(user_id:int, destination_name:int):
    return explain_recommendation(destination_name, user_id)

    