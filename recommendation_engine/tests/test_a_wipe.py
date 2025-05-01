import pymysql
import os
import pytest
from dotenv import load_dotenv
from recommendation_engine.database.create_tables import run_create_tables
from recommendation_engine.database.dummy_data import insert_dummy_data

def wipe_all_tables():
    env_path = os.path.join(os.path.dirname(__file__), '../../.env')
    load_dotenv(dotenv_path=env_path)

    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")

    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        autocommit=True
    )
    cursor = connection.cursor()

    try:
        print("[DB WIPE] Disabling foreign key checks...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

        print("[DB WIPE] Dropping all tables...")
        tables = ['user_recommendations', 'past_destinations', 'travel_costs', 'attractions', 'users', 'destinations']
        for table in tables:
            cursor.execute(f"DROP TABLE IF EXISTS {table};")
            print(f" - Dropped {table}")

        print("[DB WIPE] Enabling foreign key checks...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

    finally:
        cursor.close()
        connection.close()
        print("[DB WIPE] Database cleaned.")


@pytest.fixture(scope="session")
def wipe_and_insert():
    print("[DB RESET] Wiping all tables...")
    wipe_all_tables()

    print("[DB RESET] Recreating tables...")
    run_create_tables()

    print("[DB RESET] Inserting dummy data...")
    insert_dummy_data()

    print("[DB READY] Database is ready for tests.")
    yield
    
    

def test_wipe_and_seed_runs(wipe_and_insert):
    
    assert True