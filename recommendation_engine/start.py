import subprocess
import uvicorn
from recommendation_engine.database import create_tables, dummy_data
from recommendation_engine.recommender.data_preprocessing import run_preprocessing


def main():
    print("[Step 1] Creating database tables...")
    create_tables()

    print("[Step 2] Inserting dummy data...")
    dummy_data()

    print("[Step 3] Running data preprocessing...")
    run_preprocessing()

    print("[Step 4] Starting FastAPI server...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)