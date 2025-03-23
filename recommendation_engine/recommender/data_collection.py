import pymysql
import os
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection details
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

# Connect to MySQL database
connection = pymysql.connect(**DB_CONFIG)
cursor = connection.cursor()

# Fetch data from database
tables = {
    "users": "SELECT * FROM users;",
    "destinations": "SELECT * FROM destinations;",
    "travel_costs": "SELECT * FROM travel_costs;"
}

# Convert data to DataFrames
dfs = {}
for table, query in tables.items():
    cursor.execute(query)
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]  # Get column names
    dfs[table] = pd.DataFrame(data, columns=columns)

# Close database connection
cursor.close()
connection.close()

# Extract DataFrames
users_df = dfs["users"]
destinations_df = dfs["destinations"]
travel_costs_df = dfs["travel_costs"]

# Handle missing values
users_df.fillna({
    "age": users_df["age"].mean(),
    "preferred_destination": "Unknown",
    "past_destinations": "Unknown",
    "budget": users_df["budget"].mean()
}, inplace=True)

destinations_df.fillna({
    "currency": "Unknown",
    "climate": "Unknown",
    "terrain": "Unknown",
    "language": "Unknown"
}, inplace=True)

travel_costs_df.fillna({
    "flight_cost": travel_costs_df["flight_cost"].mean(),
    "train_cost": travel_costs_df["train_cost"].mean(),
    "hotel_cost": travel_costs_df["hotel_cost"].mean()
}, inplace=True)

# Convert data types
users_df["age"] = users_df["age"].astype(int)
users_df["budget"] = users_df["budget"].astype(float)
travel_costs_df[["flight_cost", "train_cost", "hotel_cost"]] = travel_costs_df[["flight_cost", "train_cost", "hotel_cost"]].astype(float)

# Process off-season months
month_map = {
    "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
    "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12
}

destinations_df["off_season_start"] = destinations_df["off_season_start"].map(month_map)
destinations_df["off_season_end"] = destinations_df["off_season_end"].map(month_map)

# Determine if a destination is in off-season
current_month = pd.to_datetime("today").month

def is_off_season(start, end, current):
    return start <= current <= end if start <= end else current >= start or current <= end

destinations_df["is_off_season"] = destinations_df.apply(
    lambda row: is_off_season(row["off_season_start"], row["off_season_end"], current_month), axis=1
)

# Ensure unique records
users_df.drop_duplicates(inplace=True)
destinations_df.drop_duplicates(inplace=True)
travel_costs_df.drop_duplicates(inplace=True)

# Split past destinations into lists
users_df["past_destinations"] = users_df["past_destinations"].apply(
    lambda x: x.split(",") if isinstance(x, str) else []
)

# Print sample data
print("\nUsers DataFrame:")
print(users_df.head())

print("\nDestinations DataFrame:")
print(destinations_df.head())

print("\nTravel Costs DataFrame:")
print(travel_costs_df.head())
