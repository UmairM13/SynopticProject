import subprocess
from recommendation_engine.database.create_tables import run_create_tables
from recommendation_engine.database.dummy_data import insert_dummy_data
from recommendation_engine.recommender.data_preprocessing import run_preprocessing

def main():
    print("[Step 1] Running data preprocessing...")
    run_preprocessing()

    print("[Step 2] Starting FastAPI server...")
    subprocess.run(["uvicorn", "recommendation_engine.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])

if __name__ == "__main__":
    main()
