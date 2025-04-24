import pymysql.connections
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch database connection details from environment variables
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

# Connect to the MySQL database
connection = pymysql.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

cursor = connection.cursor()

# Create Destinations table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS destinations(
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        country VARCHAR(255) NOT NULL,
        off_season_start VARCHAR(50) NOT NULL,
        off_season_end VARCHAR(50) NOT NULL,
        avg_daily_budget DECIMAL(10,2) NOT NULL,
        currency VARCHAR(10),
        climate VARCHAR(100),
        terrain VARCHAR(100),
        language VARCHAR(100),
        safety_rating DECIMAL(3,2),
        holiday_type VARCHAR(100)
    );
""")

# Create Users table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nationality VARCHAR(100),
        current_city VARCHAR(255),
        current_country VARCHAR(255),
        age INT,
        preferred_climate VARCHAR(100),
        preferred_terrain VARCHAR(100),
        past_destinations TEXT,
        budget DECIMAL(10,2),
        holiday_type VARCHAR(100),
        trip_start_date DATE,
        trip_end_date DATE,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255),
        salt VARCHAR(255),
        session_token VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""")

# Create Travel Costs table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS travel_costs( 
        id INT AUTO_INCREMENT PRIMARY KEY,
        destination_id INT NOT NULL,
        departure_city VARCHAR(255) NOT NULL,
        departure_country VARCHAR(255) NOT NULL,
        flight_cost DECIMAL(10,2),
        train_cost DECIMAL(10,2),
        hotel_cost DECIMAL(10,2),
        user_id INT NOT NULL,
        FOREIGN KEY(destination_id) REFERENCES destinations(id) ON DELETE CASCADE,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );
""")

# Create Attractions table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS attractions(
        id INT AUTO_INCREMENT PRIMARY KEY,
        destination_id INT NOT NULL,
        name VARCHAR(255) NOT NULL,
        type VARCHAR(100),
        description TEXT,
        entry_fee DECIMAL(10,2),
        FOREIGN KEY(destination_id) REFERENCES destinations(id) ON DELETE CASCADE
    );
""")


cursor.execute("""
    CREATE TABLE IF NOT EXISTS past_destinations (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        destination_name VARCHAR(255) NOT NULL,
        trip_start_date DATE,
        trip_end_date DATE,
        rating DECIMAL(3,2),
        notes TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );
""")



# Commit changes and close the connection
connection.commit()
cursor.close()
connection.close()

print("Tables created successfully in MySQL database.")
