from recommendation_engine.recommender.hybrid_recommender import recommend_destinations, explain_recommendation

def get_recommendations_for_user(user_id: int, top_n:int):
    return recommend_destinations(user_id, top_n=top_n)

def get_explanation_for_destination(user_id:int, destination_name:str):
    return explain_recommendation(user_id, destination_name)