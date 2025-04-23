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
    INSERT INTO destinations (
        name, country, off_season_start, off_season_end, avg_daily_budget, currency,
        climate, terrain, language, safety_rating, holiday_type
    ) VALUES
    ('Paris', 'France', 'November', 'February', 100.00, 'EUR', 'Temperate', 'Urban', 'French', 4.5, 'Romantic,Cultural'),
('Bali', 'Indonesia', 'May', 'October', 50.00, 'IDR', 'Tropical,Humid', 'Beach,Jungle', 'Indonesian', 4.7, 'Relaxed,Romantic'),
('Tokyo', 'Japan', 'December', 'February', 120.00, 'JPY', 'Temperate,Humid', 'Urban', 'Japanese', 4.3, 'Solo,Cultural'),
('Cape Town', 'South Africa', 'April', 'September', 80.00, 'ZAR', 'Mediterranean', 'Mountain,Coastal', 'English', 4.8, 'Adventurous,Nature'),
('Victoria Falls', 'Zimbabwe', 'March', 'June', 60.00, 'USD', 'Tropical,Humid', 'River,Jungle', 'English', 4.6, 'Adventurous,Nature'),
('New York', 'USA', 'January', 'March', 150.00, 'USD', 'Temperate', 'Urban', 'English', 4.7, 'Shopping,Solo'),
('Rome', 'Italy', 'November', 'February', 90.00, 'EUR', 'Mediterranean', 'Urban', 'Italian', 4.4, 'Cultural,Romantic'),
('Santorini', 'Greece', 'October', 'April', 110.00, 'EUR', 'Mediterranean', 'Beach,Valley', 'Greek', 4.8, 'Romantic,Relaxed'),
('Sydney', 'Australia', 'May', 'August', 130.00, 'AUD', 'Temperate', 'Urban,Coastal', 'English', 4.7, 'Family,Adventurous'),
('Reykjavik', 'Iceland', 'October', 'March', 140.00, 'ISK', 'Polar', 'Urban,Mountain', 'Icelandic', 4.5, 'Nature,Adventurous'),
('Dubai', 'UAE', 'May', 'September', 200.00, 'AED', 'Arid', 'Urban', 'Arabic', 4.6, 'Luxury,Shopping'),
('Bangkok', 'Thailand', 'June', 'October', 70.00, 'THB', 'Tropical,Humid', 'Urban', 'Thai', 4.3, 'Cultural,Party'),
('Moscow', 'Russia', 'November', 'March', 75.00, 'RUB', 'Polar', 'Urban', 'Russian', 4.2, 'Cultural'),
('Rio de Janeiro', 'Brazil', 'April', 'September', 80.00, 'BRL', 'Sub-Tropical,Coastal', 'Beach,Urban', 'Portuguese', 4.5, 'Party,Adventurous'),
('Los Angeles', 'USA', 'January', 'April', 140.00, 'USD', 'Mediterranean', 'Urban,Beach', 'English', 4.6, 'Relaxed,Shopping'),
('Cairo', 'Egypt', 'June', 'September', 60.00, 'EGP', 'Arid', 'Urban,Desert', 'Arabic', 4.1, 'Cultural,Adventurous'),
('London', 'UK', 'November', 'March', 130.00, 'GBP', 'Temperate', 'Urban', 'English', 4.7, 'Cultural,Solo'),
('Seoul', 'South Korea', 'December', 'February', 90.00, 'KRW', 'Temperate', 'Urban,Mountain', 'Korean', 4.5, 'Cultural'),
('Madrid', 'Spain', 'October', 'February', 100.00, 'EUR', 'Mediterranean', 'Urban', 'Spanish', 4.6, 'Cultural'),
('Toronto', 'Canada', 'December', 'March', 110.00, 'CAD', 'Polar', 'Urban,River', 'English', 4.4, 'Family'),
('Norwegian Fjords', 'Norway', 'October', 'March', 150.00, 'NOK', 'Polar,Coastal', 'Mountain,River', 'Norwegian', 4.7, 'Nature,Relaxed'),
('Amazon Lodge', 'Brazil', 'April', 'November', 90.00, 'BRL', 'Tropical,Humid', 'Jungle,River', 'Portuguese', 4.2, 'Adventurous,Nature'),
('Sahara Camp', 'Morocco', 'June', 'August', 70.00, 'MAD', 'Arid', 'Desert', 'Arabic', 4.4, 'Adventurous,Cultural'),
('Swiss Alps', 'Switzerland', 'June', 'September', 180.00, 'CHF', 'Alpine,Temperate', 'Mountain,Valley', 'German', 4.8, 'Luxury,Family');
""")

connection.commit()


# Insert dummy data into users first to avoid foreign key constraint errors
cursor.execute("""
    INSERT INTO users (
        nationality, current_city, current_country, age,
        preferred_climate, preferred_terrain, past_destinations, budget,
        holiday_type, email, password, salt, session_token,
        trip_start_date, trip_end_date, created_at
    ) VALUES
    ('British', 'London', 'UK', 30, 'Temperate, Mediterranean', 'Mountain, Coastal', 'Bali, Tokyo', 2000.00, 'Relaxed, Cultural', 'u1@gmail.com', 'password', 'salt', null, '2025-06-01', '2025-06-14', NOW()),
    ('Australian', 'Sydney', 'Australia', 27, 'Any', 'Beach, Jungle', 'Paris, Cape Town', 1500.00, 'Adventurous, Romantic', 'u2@gmail.com', 'password', 'salt', null, '2025-07-01', '2025-07-10', NOW()),
    ('American', 'New York', 'USA', 35, 'Tropical, Temperate', 'Urban, Beach', 'Paris, Bali', 3000.00, 'Relaxed, Shopping', 'u3@gmail.com', 'password', 'salt', null, '2025-08-01', '2025-08-15', NOW()),
    ('German', 'Berlin', 'Germany', 40, 'Polar, Alpine', 'Forest, Mountain', 'Tokyo, Bali', 2500.00, 'Adventurous, Cultural', 'u4@gmail.com', 'password', 'salt', null, '2025-09-01', '2025-09-10', NOW()),
    ('Canadian', 'Toronto', 'Canada', 28, 'Mediterranean, Temperate', 'Lake, Urban', 'Rome, Sydney', 1800.00, 'Romantic, Relaxed', 'u5@gmail.com', 'password', 'salt', null, '2025-10-01', '2025-10-07', NOW()),
    ('Japanese', 'Tokyo', 'Japan', 32, 'Polar, Temperate', 'Mountain, Urban', 'Moscow, London', 2200.00, 'Cultural, Solo', 'u6@gmail.com', 'password', 'salt', null, '2025-11-01', '2025-11-12', NOW()),
    ('French', 'Paris', 'France', 26, 'Temperate, Humid', 'Urban, Beach', 'London, Rome', 2500.00, 'Shopping, Romantic', 'u7@gmail.com', 'password', 'salt', null, '2025-12-01', '2025-12-05', NOW()),
    ('Brazilian', 'Rio de Janeiro', 'Brazil', 29, 'Mediterranean, Tropical', 'Beach, Urban', 'Barcelona, Lisbon', 1600.00, 'Cultural, Party', 'u8@gmail.com', 'password', 'salt', null, '2025-01-01', '2025-01-10', NOW()),
    ('South African', 'Cape Town', 'South Africa', 34, 'Desert, Temperate', 'Mountain, Coastal', 'Cairo, Sydney', 2700.00, 'Luxury, Adventure', 'u9@gmail.com', 'password', 'salt', null, '2025-02-01', '2025-02-07', NOW()),
    ('Russian', 'Moscow', 'Russia', 31, 'Mediterranean, Polar', 'Forest, Urban', 'London, Bangkok', 2000.00, 'Party, Cultural', 'u10@gmail.com', 'password', 'salt', null, '2025-03-01', '2025-03-05', NOW());
""")



# Commit users data first so that their IDs are available for reference in other tables
connection.commit()

# Insert dummy data into attractions
cursor.execute("""
            INSERT INTO attractions (destination_id, name, type, description, entry_fee)
            VALUES
            (1, 'Eiffel Tower', 'Monument', 'Famous iron tower in Paris.', 25.00),
            (2, 'Sacred Monkey Forest', 'Nature', 'A forest home to monkeys in Ubud.', 15.00),
            (3, 'Shibuya Crossing', 'Urban', 'Busiest pedestrian crossing in the world.', 0.00),
            (4, 'Table Mountain', 'Nature', 'Flat-topped mountain in Cape Town.', 50.00),
            (5, 'Victoria Falls', 'Nature', 'One of the largest waterfalls in the world.', 30.00),
            (6, 'Statue of Liberty', 'Monument', 'Iconic landmark in New York.', 20.00),
            (7, 'Colosseum', 'Historic', 'Ancient Roman amphitheater.', 35.00),
            (8, 'Santorini Sunsets', 'Scenic', 'Famous sunsets over whitewashed buildings.', 0.00),
            (9, 'Sydney Opera House', 'Cultural', 'Iconic performing arts center.', 40.00),
            (10, 'Blue Lagoon', 'Nature', 'Famous geothermal spa in Iceland.', 50.00);
""")

connection.commit()

# Insert dummy data into travel_costs (with valid user_id references)
cursor.execute("""
    INSERT INTO travel_costs (destination_id, departure_city, departure_country, flight_cost, train_cost, hotel_cost, user_id)
    VALUES
    (1, 'London', 'UK', 150.00, 0.00, 120.00, 1),
    (2, 'Sydney', 'Australia', 400.00, 0.00, 80.00, 2),
    (3, 'New York', 'USA', 800.00, 0.00, 180.00, 3),
    (4, 'Berlin', 'Germany', 200.00, 0.00, 100.00, 4),
    (5, 'Harare', 'Zimbabwe', 600.00, 0.00, 110.00, 5),
    (6, 'Toronto', 'Canada', 500.00, 0.00, 140.00, 6),
    (7, 'Rome', 'Italy', 250.00, 0.00, 130.00, 7),
    (8, 'Athens', 'Greece', 270.00, 0.00, 115.00, 8),
    (9, 'Melbourne', 'Australia', 450.00, 0.00, 120.00, 9),
    (10, 'Copenhagen', 'Denmark', 350.00, 0.00, 145.00, 10),
    (11, 'Dubai', 'UAE', 600.00, 0.00, 250.00, 1),
    (12, 'Bangkok', 'Thailand', 400.00, 0.00, 90.00, 2),
    (13, 'Moscow', 'Russia', 500.00, 0.00, 95.00, 3),
    (14, 'Rio de Janeiro', 'Brazil', 700.00, 0.00, 170.00, 4),
    (15, 'Los Angeles', 'USA', 800.00, 0.00, 200.00, 5),
    (16, 'Cairo', 'Egypt', 450.00, 0.00, 80.00, 6),
    (17, 'Manchester', 'UK', 130.00, 0.00, 140.00, 7),
    (18, 'Seoul', 'South Korea', 850.00, 0.00, 180.00, 8),
    (19, 'Madrid', 'Spain', 290.00, 0.00, 120.00, 9),
    (20, 'Vancouver', 'Canada', 600.00, 0.00, 150.00, 10);
""")



# Commit changes and close the connection
connection.commit()
cursor.close()
connection.close()


print("Dummy data inserted successfully!")