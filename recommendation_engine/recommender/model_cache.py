from sklearn.neighbors import NearestNeighbors
import numpy as np

class ModelCache:
    knn = None

    @classmethod
    def rebuild(cls, destinations_df):
        from recommendation_engine.recommender.data_loader import load_processed_data
        destinations_df = destinations_df.select_dtypes(include=[np.number])
        
        if not destinations_df.empty:
            cls.knn = NearestNeighbors(n_neighbors=10, metric="euclidean")
            cls.knn.fit(destinations_df)
            print(f"KNN model rebuilt with {len(destinations_df)} destinations.")
        else:
            cls.knn = None
            print("No destination data available to build KNN.")

    @classmethod
    def get_knn(cls):
        if cls.knn is None:
            raise Exception("KNN model is not built yet. Run ModelCache.rebuild first.")
        return cls.knn
