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

# Insert dummy data into destinations
cursor.execute("""
    INSERT INTO destinations (name, country, off_season_start, off_season_end, avg_daily_budget, currency, climate, terrain, language, safety_rating)
    VALUES
    ('Paris', 'France', 'November', 'February', 100.00, 'EUR', 'Temperate', 'City', 'French', 4.5),
    ('Bali', 'Indonesia', 'May', 'October', 50.00, 'IDR', 'Tropical', 'Beach', 'Indonesian', 4.7),
    ('Tokyo', 'Japan', 'December', 'February', 120.00, 'JPY', 'Temperate', 'Urban', 'Japanese', 4.3),
    ('Cape Town', 'South Africa', 'April', 'September', 80.00, 'ZAR', 'Mediterranean', 'Mountain', 'English', 4.8);
""")

connection.commit()


# Insert dummy data into users first to avoid foreign key constraint errors
cursor.execute("""
    INSERT INTO users (nationality, current_city, current_country, age, preferred_destination, past_destinations, budget, holiday_type)
    VALUES
    ('British', 'London', 'UK', 30, 'Paris', 'Bali, Tokyo', 2000.00, 'Relaxed'),
    ('Australian', 'Sydney', 'Australia', 27, 'Bali', 'Paris, Cape Town', 1500.00, 'Adventurous'),
    ('American', 'New York', 'USA', 35, 'Tokyo', 'Paris, Bali', 3000.00, 'Relaxed'),
    ('German', 'Berlin', 'Germany', 40, 'Cape Town', 'Tokyo, Bali', 2500.00, 'Adventurous');
""")

# Commit users data first so that their IDs are available for reference in other tables
connection.commit()

# Insert dummy data into attractions
cursor.execute("""
    INSERT INTO attractions (destination_id, name, type, description, entry_fee)
    VALUES
    (1, 'Eiffel Tower', 'Monument', 'Famous iron tower in Paris.', 25.00),
    (2, 'Sacred Monkey Forest Sanctuary', 'Nature', 'A forest home to hundreds of monkeys in Ubud.', 15.00),
    (3, 'Shibuya Crossing', 'Urban', 'The busiest pedestrian crossing in the world.', 0.00),
    (4, 'Table Mountain', 'Nature', 'A flat-topped mountain in Cape Town.', 50.00);
""")

connection.commit()

# Insert dummy data into travel_costs (with valid user_id references)
cursor.execute("""
    INSERT INTO travel_costs (destination_id, departure_city, departure_country, flight_cost, train_cost, hotel_cost, user_id)
    VALUES
    (1, 'London', 'UK', 150.00, 0.00, 120.00, 1),
    (2, 'Sydney', 'Australia', 400.00, 0.00, 80.00, 2),
    (3, 'New York', 'USA', 800.00, 0.00, 180.00, 3),
    (4, 'Berlin', 'Germany', 200.00, 0.00, 100.00, 4);
""")



# Commit changes and close the connection
connection.commit()
cursor.close()
connection.close()


print("Dummy data inserted successfully!")