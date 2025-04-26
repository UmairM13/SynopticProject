import pymysql
import os
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

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
    "travel_costs": "SELECT * FROM travel_costs;",
    "past_destinations": "SELECT * FROM past_destinations;"
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
past_destinations_df = dfs["past_destinations"]

# ===================== USERS =====================
users_df.fillna({
    "age": users_df["age"].mean(),
    "preferred_climate": "any",
    "preferred_terrain": "Unknown",
    "past_destinations": "Unknown",
    "holiday_type": "Unknown",
    "budget": users_df["budget"].mean(),
    "trip_start_date": datetime.now().date(),
    "trip_end_date": datetime.now().date()
}, inplace=True)

# Convert dates and calculate daily budget
users_df["trip_start_date"] = pd.to_datetime(users_df["trip_start_date"])
users_df["trip_end_date"] = pd.to_datetime(users_df["trip_end_date"])

def calculate_daily_budget(row):
    duration = (row["trip_end_date"] - row["trip_start_date"]).days
    duration = duration if duration > 0 else 7
    return row["budget"] / duration

users_df["daily_budget"] = users_df.apply(calculate_daily_budget, axis=1)

# ===================== DESTINATIONS =====================
destinations_df.fillna({
    "currency": "Unknown",
    "climate": "Unknown",
    "terrain": "Unknown",
    "language": "Unknown",
    "IATA_code": "XXX"
}, inplace=True)

# ===================== TRAVEL COSTS =====================
travel_costs_df.fillna({
    "flight_cost": travel_costs_df["flight_cost"].mean(),
    "train_cost": travel_costs_df["train_cost"].mean(),
    "hotel_cost": travel_costs_df["hotel_cost"].mean()
}, inplace=True)

# Convert numeric types
users_df["age"] = users_df["age"].astype(int)
users_df["budget"] = users_df["budget"].astype(float)
travel_costs_df[["flight_cost", "train_cost", "hotel_cost"]] = travel_costs_df[["flight_cost", "train_cost", "hotel_cost"]].astype(float)

# ===================== PAST DESTINATIONS =====================
# Convert trip_end_date to datetime and drop NaNs
past_destinations_df["trip_end_date"] = pd.to_datetime(past_destinations_df["trip_end_date"], errors='coerce')
past_destinations_df.dropna(subset=["trip_end_date", "destination_name"], inplace=True)

# ===================== OTHER CLEANUPS =====================
# Month conversion
month_map = {
    "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
    "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12
}
destinations_df["off_season_start"] = destinations_df["off_season_start"].map(month_map)
destinations_df["off_season_end"] = destinations_df["off_season_end"].map(month_map)

# Ensure unique records
users_df.drop_duplicates(inplace=True)
destinations_df.drop_duplicates(inplace=True)
travel_costs_df.drop_duplicates(inplace=True)
past_destinations_df.drop_duplicates(inplace=True)

# Clean up past_destinations inside users
users_df["past_destinations"] = users_df["past_destinations"].fillna('')
users_df["past_destinations"] = users_df["past_destinations"].apply(
    lambda x: [item.strip() for item in x.split(',')] if isinstance(x, str) and x.strip() else []
)

# Merge travel cost into destinations
destinations_df = pd.merge(
    destinations_df,
    travel_costs_df,
    left_on="id",
    right_on="destination_id",
    how="left"
)
for col in ["flight_cost", "train_cost", "hotel_cost"]:
    destinations_df[col] = destinations_df[col].fillna(destinations_df[col].median())

destinations_df.drop(columns=["id_y"], inplace=True, errors="ignore")
destinations_df.rename(columns={"id_x": "id"}, inplace=True)

# Save location
current_directory = os.path.dirname(os.path.realpath(__file__))
processed_data_dir = os.path.join(current_directory, 'processed_data')
os.makedirs(processed_data_dir, exist_ok=True)

print("Data collection complete.")
