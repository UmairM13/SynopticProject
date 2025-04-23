import pymysql
import os
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
import ast

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

# Handle missing values for users
users_df.fillna({
    "age": users_df["age"].mean(),
    "preferred_climate": "any",  # Handle 'any' climate
    "preferred_terrain": "Unknown",  # Handle missing preferred_terrain
    "past_destinations": "Unknown",
    "holiday_type": "Unknown",
    "budget": users_df["budget"].mean(),
    "trip_start_date": datetime.now().date(),  # Assign current date if missing
    "trip_end_date": datetime.now().date()  # Assign current date if missing
}, inplace=True)

# Estimate daily budget by calculating the duration if dates are available
def calculate_daily_budget(row):
    if pd.isna(row["trip_start_date"]) or pd.isna(row["trip_end_date"]):
        # If dates are missing, assume a default trip duration (7 days)
        duration = 7
    else:
        trip_duration = (row["trip_end_date"] - row["trip_start_date"]).days
        duration = trip_duration if trip_duration > 0 else 7  # Ensure positive duration

    return row["budget"] / duration

# Convert dates to datetime and calculate daily budget
users_df["trip_start_date"] = pd.to_datetime(users_df["trip_start_date"])
users_df["trip_end_date"] = pd.to_datetime(users_df["trip_end_date"])
users_df["daily_budget"] = users_df.apply(calculate_daily_budget, axis=1)

# Handle missing values for destinations
destinations_df.fillna({
    "currency": "Unknown",
    "climate": "Unknown",
    "terrain": "Unknown",
    "language": "Unknown"
}, inplace=True)

# Handle missing values for travel costs
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

# Ensure unique records
users_df.drop_duplicates(inplace=True)
destinations_df.drop_duplicates(inplace=True)
travel_costs_df.drop_duplicates(inplace=True)

# Split past destinations into lists
users_df['past_destinations'] = users_df['past_destinations'].fillna('')
users_df['past_destinations'] = users_df['past_destinations'].apply(
    lambda x: [item.strip() for item in x.split(',')] if isinstance(x, str) and x.strip() != '' else []
)
# Merge destinations with travel costs
destinations_df = pd.merge(
    destinations_df,
    travel_costs_df,
    left_on="id",  
    right_on="destination_id",
    how="left"
)

cost_columns = ["flight_cost", "train_cost", "hotel_cost"]
for col in cost_columns:
    destinations_df[col] = destinations_df[col].fillna(
        destinations_df[col].median()
    )
    
    
# Clean up merge artifacts
destinations_df = destinations_df.drop(columns=["id_y"], errors="ignore").rename(columns={"id_x": "id"})

# Get the current directory of the script
current_directory = os.path.dirname(os.path.realpath(__file__))

# Define the 'processed_data' folder path within the current directory
processed_data_dir = os.path.join(current_directory, 'processed_data')

# Create the 'processed_data' folder if it doesn't exist
os.makedirs(processed_data_dir, exist_ok=True)

# Print sample data
# print("\nUsers DataFrame:")
# print(users_df.head())

# print("\nDestinations DataFrame:")
# print(destinations_df.head())

# print("\nTravel Costs DataFrame:")
# print(travel_costs_df.head())

print("Data collection complete.")
