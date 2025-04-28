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
    climate, terrain, language, safety_rating, holiday_type, IATA_code
    ) VALUES
    ('Paris', 'France', 'November', 'February', 100.00, 'EUR', 'Temperate', 'Urban', 'French', 4.5, 'Romantic,Cultural', 'PAR'),
    ('Bali', 'Indonesia', 'May', 'October', 50.00, 'IDR', 'Tropical,Humid', 'Beach,Jungle', 'Indonesian', 4.7, 'Relaxed,Romantic', 'DPS'),
    ('Tokyo', 'Japan', 'December', 'February', 120.00, 'JPY', 'Temperate,Humid', 'Urban', 'Japanese', 4.3, 'Solo,Cultural', 'TYO'),
    ('Cape Town', 'South Africa', 'April', 'September', 80.00, 'ZAR', 'Mediterranean', 'Mountain,Coastal', 'English', 4.8, 'Adventurous,Nature', 'CPT'),
    ('Victoria Falls', 'Zimbabwe', 'March', 'June', 60.00, 'USD', 'Tropical,Humid', 'River,Jungle', 'English', 4.6, 'Adventurous,Nature', 'VFA'),
    ('New York', 'USA', 'January', 'March', 150.00, 'USD', 'Temperate', 'Urban', 'English', 4.7, 'Shopping,Solo', 'NYC'),
    ('Rome', 'Italy', 'November', 'February', 90.00, 'EUR', 'Mediterranean', 'Urban', 'Italian', 4.4, 'Cultural,Romantic', 'ROM'),
    ('Santorini', 'Greece', 'October', 'April', 110.00, 'EUR', 'Mediterranean', 'Beach,Valley', 'Greek', 4.8, 'Romantic,Relaxed', 'JTR'),
    ('Sydney', 'Australia', 'May', 'August', 130.00, 'AUD', 'Temperate', 'Urban,Coastal', 'English', 4.7, 'Family,Adventurous', 'SYD'),
    ('Reykjavik', 'Iceland', 'October', 'March', 140.00, 'ISK', 'Polar', 'Urban,Mountain', 'Icelandic', 4.5, 'Nature,Adventurous', 'REK'),
    ('Dubai', 'UAE', 'May', 'September', 200.00, 'AED', 'Arid', 'Urban', 'Arabic', 4.6, 'Luxury,Shopping', 'DXB'),
    ('Bangkok', 'Thailand', 'June', 'October', 70.00, 'THB', 'Tropical,Humid', 'Urban', 'Thai', 4.3, 'Cultural,Party', 'BKK'),
    ('Moscow', 'Russia', 'November', 'March', 75.00, 'RUB', 'Polar', 'Urban', 'Russian', 4.2, 'Cultural', 'MOW'),
    ('Rio de Janeiro', 'Brazil', 'April', 'September', 80.00, 'BRL', 'Sub-Tropical,Coastal', 'Beach,Urban', 'Portuguese', 4.5, 'Party,Adventurous', 'RIO'),
    ('Los Angeles', 'USA', 'January', 'April', 140.00, 'USD', 'Mediterranean', 'Urban,Beach', 'English', 4.6, 'Relaxed,Shopping', 'LAX'),
    ('Cairo', 'Egypt', 'June', 'September', 60.00, 'EGP', 'Arid', 'Urban,Desert', 'Arabic', 4.1, 'Cultural,Adventurous', 'CAI'),
    ('London', 'UK', 'November', 'March', 130.00, 'GBP', 'Temperate', 'Urban', 'English', 4.7, 'Cultural,Solo', 'LON'),
    ('Seoul', 'South Korea', 'December', 'February', 90.00, 'KRW', 'Temperate', 'Urban,Mountain', 'Korean', 4.5, 'Cultural', 'SEL'),
    ('Madrid', 'Spain', 'October', 'February', 100.00, 'EUR', 'Mediterranean', 'Urban', 'Spanish', 4.6, 'Cultural', 'MAD'),
    ('Toronto', 'Canada', 'December', 'March', 110.00, 'CAD', 'Polar', 'Urban,River', 'English', 4.4, 'Family', 'YTO'),
    ('Norwegian Fjords', 'Norway', 'October', 'March', 150.00, 'NOK', 'Polar,Coastal', 'Mountain,River', 'Norwegian', 4.7, 'Nature,Relaxed', 'BGO'), -- Bergen Airport, best match
    ('Amazon Lodge', 'Brazil', 'April', 'November', 90.00, 'BRL', 'Tropical,Humid', 'Jungle,River', 'Portuguese', 4.2, 'Adventurous,Nature', 'MAO'), -- Manaus Airport
    ('Sahara Camp', 'Morocco', 'June', 'August', 70.00, 'MAD', 'Arid', 'Desert', 'Arabic', 4.4, 'Adventurous,Cultural', 'RAK'), -- Marrakesh Airport (closest for desert tours)
    ('Swiss Alps', 'Switzerland', 'June', 'September', 180.00, 'CHF', 'Alpine,Temperate', 'Mountain,Valley', 'German', 4.8, 'Luxury,Family', 'ZRH'), -- Zurich Airport
    ('Prague', 'Czech Republic', 'November', 'February', 80.00, 'CZK', 'Temperate', 'Urban', 'Czech', 4.5, 'Cultural,Romantic', 'PRG'),
    ('Marrakech', 'Morocco', 'June', 'September', 70.00, 'MAD', 'Arid', 'Urban,Desert', 'Arabic', 4.4, 'Cultural,Shopping', 'RAK'),
    ('Cusco', 'Peru', 'January', 'March', 60.00, 'PEN', 'Alpine,Temperate', 'Mountain,Valley', 'Spanish', 4.6, 'Adventurous,Cultural', 'CUZ'),
    ('Queenstown', 'New Zealand', 'May', 'August', 120.00, 'NZD', 'Temperate', 'Mountain,River', 'English', 4.9, 'Adventurous,Nature', 'ZQN'),
    ('Havana', 'Cuba', 'June', 'September', 65.00, 'CUP', 'Tropical,Humid', 'Urban,Coastal', 'Spanish', 4.3, 'Cultural,Relaxed', 'HAV'),
    ('Petra', 'Jordan', 'May', 'September', 75.00, 'JOD', 'Arid', 'Desert,Mountain', 'Arabic', 4.7, 'Cultural,Adventurous', 'AMM'), -- via Amman Airport
    ('Siem Reap', 'Cambodia', 'April', 'October', 55.00, 'KHR', 'Tropical,Humid', 'Urban,Jungle', 'Khmer', 4.4, 'Cultural,Nature', 'REP'),
    ('Banff', 'Canada', 'October', 'March', 140.00, 'CAD', 'Alpine,Temperate', 'Mountain,River', 'English', 4.9, 'Nature,Relaxed', 'YYC'), -- via Calgary Airport
    ('Edinburgh', 'UK', 'November', 'March', 100.00, 'GBP', 'Temperate', 'Urban,Mountain', 'English', 4.6, 'Cultural,Romantic', 'EDI'),
    ('Zanzibar', 'Tanzania', 'March', 'May', 80.00, 'TZS', 'Tropical,Humid', 'Beach', 'Swahili', 4.5, 'Relaxed,Romantic', 'ZNZ'),
    ('Buenos Aires', 'Argentina', 'June', 'September', 70.00, 'ARS', 'Temperate', 'Urban', 'Spanish', 4.5, 'Cultural,Party', 'EZE'),
    ('Hoi An', 'Vietnam', 'October', 'February', 45.00, 'VND', 'Tropical,Humid', 'Urban,River', 'Vietnamese', 4.6, 'Cultural,Relaxed', 'DAD'), -- via Da Nang Airport
    ('Phuket', 'Thailand', 'May', 'October', 60.00, 'THB', 'Tropical,Humid', 'Beach', 'Thai', 4.4, 'Relaxed,Party', 'HKT'),
    ('Dubrovnik', 'Croatia', 'November', 'March', 90.00, 'HRK', 'Mediterranean', 'Urban,Coastal', 'Croatian', 4.7, 'Cultural,Romantic', 'DBV'),
    ('Tallinn', 'Estonia', 'November', 'February', 70.00, 'EUR', 'Temperate', 'Urban,Coastal', 'Estonian', 4.5, 'Cultural,Romantic', 'TLL'),
    ('Kigali', 'Rwanda', 'March', 'May', 65.00, 'RWF', 'Tropical', 'Urban', 'Kinyarwanda', 4.3, 'Cultural,Nature', 'KGL'),
    ('Zermatt', 'Switzerland', 'April', 'June', 160.00, 'CHF', 'Alpine,Temperate', 'Mountain,Valley', 'German', 4.9, 'Luxury,Nature', 'GVA'), -- via Geneva Airport
    ('Oaxaca', 'Mexico', 'May', 'September', 55.00, 'MXN', 'Tropical,Arid', 'Urban,Mountain', 'Spanish', 4.5, 'Cultural,Relaxed', 'OAX'),
    ('Amalfi Coast', 'Italy', 'October', 'March', 120.00, 'EUR', 'Mediterranean', 'Coastal', 'Italian', 4.8, 'Romantic,Relaxed', 'NAP'), -- via Naples
    ('Tbilisi', 'Georgia', 'November', 'March', 50.00, 'GEL', 'Temperate,Continental', 'Urban', 'Georgian', 4.4, 'Cultural,Relaxed', 'TBS'),
    ('Cartagena', 'Colombia', 'May', 'November', 60.00, 'COP', 'Tropical,Humid', 'Beach,Urban', 'Spanish', 4.5, 'Cultural,Relaxed', 'CTG'),
    ('Doha', 'Qatar', 'May', 'September', 140.00, 'QAR', 'Arid', 'Urban,Desert', 'Arabic', 4.6, 'Luxury,Cultural', 'DOH'),
    ('Ushuaia', 'Argentina', 'April', 'September', 90.00, 'ARS', 'Polar', 'Mountain,Coastal', 'Spanish', 4.3, 'Adventurous,Nature', 'USH'),
    ('Kotor', 'Montenegro', 'November', 'March', 80.00, 'EUR', 'Mediterranean', 'Coastal,Mountain', 'Montenegrin', 4.5, 'Relaxed,Cultural', 'TGD'), -- via Podgorica
    ('Muscat', 'Oman', 'May', 'September', 100.00, 'OMR', 'Arid', 'Urban,Coastal', 'Arabic', 4.7, 'Cultural,Nature', 'MCT');
    
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
    ('Russian', 'Moscow', 'Russia', 31, 'Mediterranean, Polar', 'Forest, Urban', 'London, Bangkok', 2000.00, 'Party, Cultural', 'u10@gmail.com', 'password', 'salt', null, '2025-03-01', '2025-03-05', NOW()),
    ('Indian', 'Mumbai', 'India', 29, 'Tropical, Humid', 'Urban, Coastal', 'Dubai, Bali', 1800.00, 'Relaxed, Cultural', 'u11@gmail.com', 'password', 'salt', null, '2025-04-01', '2025-04-10', NOW()),
    ('Chinese', 'Shanghai', 'China', 33, 'Temperate, Humid', 'Urban, Mountain', 'Tokyo, Seoul', 2200.00, 'Shopping, Solo', 'u12@gmail.com', 'password', 'salt', null, '2025-05-01', '2025-05-15', NOW()),
    ('Egyptian', 'Cairo', 'Egypt', 36, 'Arid, Tropical', 'Desert, Urban', 'Dubai, Marrakech', 1400.00, 'Cultural, Adventurous', 'u13@gmail.com', 'password', 'salt', null, '2025-06-01', '2025-06-08', NOW()),
    ('Mexican', 'Mexico City', 'Mexico', 27, 'Tropical, Temperate', 'Urban, Mountain', 'Los Angeles, Cancun', 1600.00, 'Party, Cultural', 'u14@gmail.com', 'password', 'salt', null, '2025-07-01', '2025-07-12', NOW()),
    ('Italian', 'Rome', 'Italy', 30, 'Mediterranean', 'Urban, Coastal', 'Paris, Madrid', 1900.00, 'Romantic, Cultural', 'u15@gmail.com', 'password', 'salt', null, '2025-08-01', '2025-08-07', NOW()),
    ('Spanish', 'Barcelona', 'Spain', 25, 'Mediterranean', 'Urban, Beach', 'London, Lisbon', 1700.00, 'Relaxed, Cultural', 'u16@gmail.com', 'password', 'salt', null, '2025-09-01', '2025-09-09', NOW()),
    ('South Korean', 'Seoul', 'South Korea', 32, 'Temperate', 'Urban, Mountain', 'Tokyo, Bangkok', 2100.00, 'Shopping, Solo', 'u17@gmail.com', 'password', 'salt', null, '2025-10-01', '2025-10-14', NOW()),
    ('Moroccan', 'Marrakech', 'Morocco', 28, 'Arid, Tropical', 'Desert, Urban', 'Cairo, Dubai', 1500.00, 'Adventurous, Cultural', 'u18@gmail.com', 'password', 'salt', null, '2025-11-01', '2025-11-07', NOW()),
    ('Indonesian', 'Jakarta', 'Indonesia', 35, 'Tropical, Humid', 'Urban, Beach', 'Bali, Phuket', 1300.00, 'Relaxed, Party', 'u19@gmail.com', 'password', 'salt', null, '2025-12-01', '2025-12-10', NOW()),
    ('Vietnamese', 'Hanoi', 'Vietnam', 24, 'Tropical, Humid', 'Urban, Mountain', 'Hoi An, Bangkok', 1100.00, 'Relaxed, Cultural', 'u20@gmail.com', 'password', 'salt', null, '2026-01-01', '2026-01-06', NOW()),
    ('Portuguese', 'Lisbon', 'Portugal', 31, 'Mediterranean', 'Urban, Coastal', 'Barcelona, Rome', 1800.00, 'Cultural, Relaxed', 'u21@gmail.com', 'password', 'salt', null, '2026-02-01', '2026-02-10', NOW()),
    ('Turkish', 'Istanbul', 'Turkey', 29, 'Mediterranean, Temperate', 'Urban, Coastal', 'Cairo, Athens', 1600.00, 'Cultural, Romantic', 'u22@gmail.com', 'password', 'salt', null, '2026-03-01', '2026-03-08', NOW()),
    ('Chilean', 'Santiago', 'Chile', 34, 'Temperate', 'Urban, Mountain', 'Buenos Aires, Rio de Janeiro', 1900.00, 'Party, Relaxed', 'u23@gmail.com', 'password', 'salt', null, '2026-04-01', '2026-04-15', NOW()),
    ('Thai', 'Bangkok', 'Thailand', 26, 'Tropical, Humid', 'Urban, Beach', 'Phuket, Bali', 1400.00, 'Party, Relaxed', 'u24@gmail.com', 'password', 'salt', null, '2026-05-01', '2026-05-10', NOW()),
    ('Kenyan', 'Nairobi', 'Kenya', 30, 'Tropical', 'Urban, Mountain', 'Cape Town, Kigali', 1700.00, 'Nature, Adventure', 'u25@gmail.com', 'password', 'salt', null, '2026-06-01', '2026-06-12', NOW()),
    ('Dutch', 'Amsterdam', 'Netherlands', 33, 'Temperate', 'Urban, River', 'London, Paris', 2200.00, 'Cultural, Relaxed', 'u26@gmail.com', 'password', 'salt', null, '2026-07-01', '2026-07-07', NOW()),
    ('Polish', 'Warsaw', 'Poland', 29, 'Temperate, Continental', 'Urban, Forest', 'Berlin, Prague', 1400.00, 'Cultural, Solo', 'u27@gmail.com', 'password', 'salt', null, '2026-08-01', '2026-08-08', NOW()),
    ('Greek', 'Athens', 'Greece', 31, 'Mediterranean', 'Urban, Coastal', 'Santorini, Rome', 1900.00, 'Romantic, Cultural', 'u28@gmail.com', 'password', 'salt', null, '2026-09-01', '2026-09-10', NOW()),
    ('Icelander', 'Reykjavik', 'Iceland', 27, 'Polar, Temperate', 'Mountain, Coastal', 'London, Oslo', 2500.00, 'Nature, Adventure', 'u29@gmail.com', 'password', 'salt', null, '2026-10-01', '2026-10-14', NOW()),
    ('Singaporean', 'Singapore', 'Singapore', 30, 'Tropical, Humid', 'Urban, Coastal', 'Bali, Tokyo', 3000.00, 'Shopping, Relaxed', 'u30@gmail.com', 'password', 'salt', null, '2026-11-01', '2026-11-09', NOW());
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

# Insert dummy data into past_destinations table
cursor.execute("""
    INSERT INTO past_destinations (user_id, destination_name, trip_start_date, trip_end_date, rating, notes) VALUES
    (1, 'Bali', '2024-06-07', '2024-06-15', 4.8, 'Great nature and local food'),
    (1, 'Tokyo', '2023-12-10', '2023-12-20', 4.6, 'Loved the culture and efficiency'),

    (2, 'Paris', '2023-07-01', '2023-07-10', 4.5, 'Eiffel Tower was amazing'),
    (2, 'Cape Town', '2022-11-25', '2022-12-05', 4.2, 'Loved the landscapes and people'),

    (3, 'Paris', '2022-09-03', '2022-09-12', 4.0, 'Charming, but too crowded in peak season'),
    (3, 'Bali', '2024-01-12', '2024-01-22', 4.7, 'Perfect for beach and food'),

    (4, 'Tokyo', '2023-04-08', '2023-04-18', 4.6, 'Cherry blossom season was magical'),
    (4, 'Bali', '2023-07-29', '2023-08-08', 4.3, 'Nice surf and scenic hikes'),

    (5, 'Rome', '2024-01-31', '2024-02-10', 4.1, 'Historical sights were amazing'),
    (5, 'Sydney', '2023-11-13', '2023-11-23', 4.4, 'Laid-back lifestyle, loved the beaches'),

    (6, 'Moscow', '2023-09-21', '2023-10-01', 3.9, 'Cold but beautiful'),
    (6, 'London', '2022-05-05', '2022-05-15', 4.0, 'Enjoyed the museums and markets'),

    (7, 'London', '2023-05-30', '2023-06-09', 4.2, 'Great shopping and shows'),
    (7, 'Rome', '2022-11-19', '2022-11-29', 4.1, 'Nice vibe, lots of tourists though'),

    (8, 'Barcelona', '2023-03-02', '2023-03-12', 4.5, 'Energetic city with great nightlife'),
    (8, 'Lisbon', '2023-06-10', '2023-06-20', 4.3, 'Good food, scenic views'),

    (9, 'Cairo', '2023-07-22', '2023-08-01', 4.4, 'Hot but incredible historical sites'),
    (9, 'Sydney', '2024-03-05', '2024-03-15', 4.6, 'Epic coastal drives'),

    (10, 'London', '2023-08-24', '2023-09-03', 4.0, 'Museum hopping was fun'),
    (10, 'Bangkok', '2024-01-09', '2024-01-19', 4.2, 'Loved the street food and markets'),
    
    (11, 'Dubai', '2023-11-10', '2023-11-18', 4.5, 'Luxury shopping and desert safari'),
    (11, 'Santorini', '2022-06-15', '2022-06-22', 4.7, 'Unforgettable sunsets and whitewashed villages'),

    (12, 'New York', '2024-04-03', '2024-04-10', 4.4, 'Times Square was electric!'),
    (12, 'Cairo', '2023-09-18', '2023-09-28', 4.2, 'Seeing the pyramids was a dream come true'),

    (13, 'Bangkok', '2023-05-05', '2023-05-15', 4.6, 'Street food paradise'),
    (13, 'Dubai', '2022-12-01', '2022-12-10', 4.3, 'Amazing skyscrapers and malls'),

    (14, 'Rio de Janeiro', '2023-02-20', '2023-03-01', 4.7, 'Carnival was wild and colorful'),
    (14, 'Amazon Lodge', '2023-07-05', '2023-07-15', 4.5, 'Incredible wildlife and river tours'),

    (15, 'Los Angeles', '2022-08-12', '2022-08-22', 4.1, 'Fun beaches and Hollywood tours'),
    (15, 'Sydney', '2023-01-17', '2023-01-27', 4.5, 'Bondi Beach lived up to the hype'),

    (16, 'Victoria Falls', '2023-03-20', '2023-03-30', 4.6, 'Majestic waterfalls and safaris'),
    (16, 'Cape Town', '2022-12-10', '2022-12-20', 4.8, 'Table Mountain hike was unforgettable'),

    (17, 'Reykjavik', '2022-10-05', '2022-10-15', 4.5, 'Northern lights were mesmerizing'),
    (17, 'Swiss Alps', '2023-02-10', '2023-02-20', 4.9, 'Skiing in a winter wonderland'),

    (18, 'Seoul', '2023-06-12', '2023-06-20', 4.4, 'Modern city with deep traditions'),
    (18, 'Tokyo', '2024-03-03', '2024-03-13', 4.7, 'Best food of my life'),

    (19, 'Madrid', '2023-04-18', '2023-04-28', 4.2, 'Laid-back vibe and delicious tapas'),
    (19, 'Rome', '2023-09-02', '2023-09-12', 4.5, 'History on every street'),

    (20, 'Toronto', '2023-05-01', '2023-05-10', 4.3, 'Vibrant city and friendly people'),
    (20, 'New York', '2022-11-15', '2022-11-25', 4.6, 'Central Park in fall is gorgeous'),
    (1, 'Reykjavik', '2023-01-15', '2023-01-25', 4.7, 'Northern lights and frozen landscapes — unforgettable'),
    (2, 'Amazon Lodge', '2023-05-20', '2023-05-30', 4.5, 'Rainy season but amazing biodiversity'),
    (3, 'Norwegian Fjords', '2022-11-10', '2022-11-20', 4.8, 'Dramatic landscapes in the quiet season'),
    (4, 'Cairo', '2023-07-05', '2023-07-15', 4.2, 'Very hot but less crowded at the pyramids'),
    (5, 'Dubai', '2023-08-10', '2023-08-18', 4.3, 'Extreme heat but incredible shopping deals'),
    (6, 'Bangkok', '2023-09-01', '2023-09-10', 4.4, 'Monsoon season but vibrant and alive'),
    (7, 'Santorini', '2023-02-01', '2023-02-10', 4.6, 'Quiet island life, perfect for relaxation'),
    (8, 'Victoria Falls', '2024-06-10', '2024-06-20', 4.7, 'High water levels made the falls even more spectacular'),
    (9, 'Seoul', '2023-01-10', '2023-01-20', 4.5, 'Winter snow made the palaces look magical'),
    (10, 'Moscow', '2023-12-01', '2023-12-10', 4.3, 'Cold but beautiful snowy streets and festive vibes');
""")


cursor.execute("""
    INSERT INTO user_recommendations (user_id, destination_id, destination_name, explanation, created_at) VALUES
    (1, 2, 'Bali', 'Saved for future surf and relaxation trip.', '2024-04-05 14:23:00'),
    (1, 7, 'Rome', 'Fascinated by the history and architecture.', '2024-04-10 10:15:00'),
    (2, 3, 'Tokyo', 'Bucket list for spring cherry blossoms.', '2024-03-20 09:00:00'),
    (2, 5, 'Cape Town', 'Loved the idea of combining beach and mountain hikes.', '2024-04-01 16:45:00'),
    (3, 1, 'Paris', 'Always wanted to visit the Louvre.', '2024-03-28 12:30:00'),
    (3, 10, 'Reykjavik', 'Northern Lights adventure dream.', '2024-05-02 11:15:00'),
    (4, 4, 'Cape Town', 'Heard great things about Table Mountain.', '2024-04-17 15:00:00'),
    (4, 11, 'Dubai', 'Modern city vibe with luxury shopping.', '2024-05-06 09:30:00'),
    (5, 8, 'Santorini', 'Romantic getaway idea.', '2024-05-10 14:50:00'),
    (5, 17, 'London', 'Love for British history and culture.', '2024-05-15 08:45:00'),
    (6, 18, 'Seoul', 'City life and Korean food adventure.', '2024-04-25 10:00:00'),
    (6, 6, 'New York', 'Saved for a big city dream trip.', '2024-05-01 13:00:00'),
    (7, 14, 'Los Angeles', 'Relaxed holiday with sunny beaches.', '2024-04-30 17:20:00'),
    (8, 13, 'Rio de Janeiro', 'Carnival experience and coastal beauty.', '2024-03-30 18:45:00'),
    (9, 12, 'Bangkok', 'Vibrant street food scene.', '2024-04-12 11:05:00'),
    (9, 16, 'Cairo', 'Curious about ancient pyramids.', '2024-05-05 16:15:00'),
    (10, 20, 'Toronto', 'Explore a multicultural city.', '2024-04-08 09:50:00'),
    (10, 21, 'Norwegian Fjords', 'Saved for a scenic nature cruise.', '2024-04-22 07:30:00'),
    (3, 9, 'Sydney', 'Love for coastal cities.', '2024-04-15 15:40:00'),
    (2, 19, 'Madrid', 'Experience Spanish culture and food.', '2024-05-03 11:55:00');
""")


# Commit changes and close the connection
connection.commit()
cursor.close()
connection.close()


print("Dummy data inserted successfully!")