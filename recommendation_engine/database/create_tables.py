import sqlite3

conn = sqlite3.connect('../db.sqlite')
cursor = conn.cursor()


### Create the Destinations table
cursor.execute(
    """
               CREATE TABLE IF NOT EXISTS destinations(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL,
               country TEXT NOT NULL,
               off_season_start TEXT NOT NULL,
               off_season_end TEXT NOT NULL,
               avg_daily_budget REAL NOT NULL,
               currency TEXT ,
               climate TEXT ,
               terrain TEXT,
               language TEXT,
               safety_rating REAL);
               """) 


### Create the travel cost table
cursor.execute(
    """
               CREATE TABLE IF NOT EXISTS travel_costs( 
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               destination_id INTEGER NOT NULL,
               departure_city TEXT NOT NULL,
               departure_country TEXT NOT NULL,
               flight_cost REAL,
               train_cost REAL,
               hotel_cost REAL,
               user_id INTEGER NOT NULL,
               FOREIGN KEY(destination_id) REFERENCES destinations(id)
               FOREIGN KEY(user_id) REFERENCES users(id)
               );
                """) 


### Create attractions table
cursor.execute(
    """
               CREATE TABLE IF NOT EXISTS attractions(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                destination_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                type TEXT,
                description TEXT,
                entry_fee REAL,
                FOREIGN KEY(destination_id) REFERENCES destinations(id)
                );
                """) 


### Create the user table
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nationality TEXT,
    current_city TEXT,
    current_country TEXT,
    age INTEGER,
    preferred_destination TEXT,
    past_destinations TEXT,
    budget REAL,
    holiday_type TEXT
);
"""
)

conn.commit()
conn.close()

print("Tables created successfully")
