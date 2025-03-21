import pymysql
import os
import pandas as pd
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Database connection details
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

# Create cursor to execute SQL queries
cursor = connection.cursor()

# Fetch all user data
cursor.execute("SELECT * FROM users;")
users_data = cursor.fetchall()

# Fetch all destination data
cursor.execute("SELECT * FROM destinations;")
destinations_data = cursor.fetchall()

# Fetch all travel cost data
cursor.execute("SELECT * FROM travel_costs;")
travel_costs_data = cursor.fetchall()

# Convert the fetched data into pandas DataFrames for easier analysis
users_df = pd.DataFrame(users_data, columns=['id', 'nationality', 'current_city', 'current_country', 'age', 'preferred_destination', 'past_destinations', 'budget', 'holiday_type'])
destinations_df = pd.DataFrame(destinations_data, columns=['id', 'name', 'country', 'off_season_start', 'off_season_end', 'avg_daily_budget', 'currency', 'climate', 'terrain', 'language', 'safety_rating'])
travel_costs_df = pd.DataFrame(travel_costs_data, columns=['id', 'destination_id', 'departure_city', 'departure_country', 'flight_cost', 'train_cost', 'hotel_cost', 'user_id'])

# Close the cursor and connection
cursor.close()
connection.close()

# Print the first few rows of each DataFrame to understand their structure
print("Users DataFrame:")
print(users_df.head())

print("\nDestinations DataFrame:")
print(destinations_df.head())

print("\nTravel Costs DataFrame:")
print(travel_costs_df.head())


print("Missing values in Users DataFrame:")
print(users_df.isnull().sum())

print("\nMissing values in Destinations DataFrame:")
print(destinations_df.isnull().sum())

print("\nMissing values in Travel Costs DataFrame:")
print(travel_costs_df.isnull().sum())


# Fill missing values in the DataFrames
users_df.fillna({'age': users_df['age'].mean(), 'preferred_destination': 'Unknown', 'past_destinations': 'Unknown'}, inplace=True)
destinations_df.fillna({'currency': 'Unknown', 'climate': 'Unknown', 'terrain': 'Unknown', 'language': 'Unknown'}, inplace=True)
travel_costs_df.fillna({'flight_cost': travel_costs_df['flight_cost'].mean(), 'train_cost': travel_costs_df['train_cost'].mean(), 'hotel_cost': travel_costs_df['hotel_cost'].mean()}, inplace=True)


print('\nMissing values after handling:')
print("Users DataFrame:")
print(users_df.isnull().sum())

print("\nDestinations DataFrame:")
print(destinations_df.isnull().sum())

print("\nTravel Costs DataFrame:")
print(travel_costs_df.isnull().sum())


# Mapping month names to a standard date format (using the 1st of each month)
month_map = {
    'January': '2025-01-01', 'February': '2025-02-01', 'March': '2025-03-01',
    'April': '2025-04-01', 'May': '2025-05-01', 'June': '2025-06-01',
    'July': '2025-07-01', 'August': '2025-08-01', 'September': '2025-09-01',
    'October': '2025-10-01', 'November': '2025-11-01', 'December': '2025-12-01'
}

destinations_df['off_season_start'] = destinations_df['off_season_start'].map(month_map)
destinations_df['off_season_end'] = destinations_df['off_season_end'].map(month_map)

# Convert columns to appropriate data types
users_df['age'] = users_df['age'].astype(int)
users_df['budget'] = users_df['budget'].astype(float)

destinations_df['off_season_start'] = pd.to_datetime(destinations_df['off_season_start'])
destinations_df['off_season_end'] = pd.to_datetime(destinations_df['off_season_end'])
destinations_df["off_season_start"] = pd.to_datetime(destinations_df["off_season_start"]).apply(lambda x: x.month)
destinations_df["off_season_end"] = pd.to_datetime(destinations_df["off_season_end"]).apply(lambda x: x.month)


travel_costs_df['flight_cost'] = travel_costs_df['flight_cost'].astype(float)
travel_costs_df['train_cost'] = travel_costs_df['train_cost'].astype(float)
travel_costs_df['hotel_cost'] = travel_costs_df['hotel_cost'].astype(float)


# remove duplicates
users_df.drop_duplicates(inplace=True)
destinations_df.drop_duplicates(inplace=True)
travel_costs_df.drop_duplicates(inplace=True)

# change to get user preference when traveling
def is_off_season(start_month, end_month, current_month):
    # Case 1: Standard off-season range within the same year (e.g., April–September)
    if start_month <= end_month:
        return start_month <= current_month <= end_month
    
    # Case 2: Off-season period spans two years (e.g., November–January)
    else:
        return current_month >= start_month or current_month <= end_month

# Get the current month
current_month = pd.to_datetime('today').month

# Apply the function to determine off-season status
destinations_df['is_off_season'] = destinations_df.apply(
    lambda row: is_off_season(row['off_season_start'], row['off_season_end'], current_month), axis=1
)

# Safer filling for budget and costs
users_df['budget'].fillna(users_df['budget'].mean() if not users_df['budget'].isna().all() else 0, inplace=True)
travel_costs_df.fillna({'flight_cost': travel_costs_df['flight_cost'].mean() or 0,
                         'train_cost': travel_costs_df['train_cost'].mean() or 0,
                         'hotel_cost': travel_costs_df['hotel_cost'].mean() or 0}, inplace=True)

# Split past destinations if stored as a string
users_df['past_destinations'] = users_df['past_destinations'].apply(lambda x: x.split(',') if isinstance(x, str) else [])

print("\nDestinations DataFrame with Corrected Off-Season Flag:")
print(destinations_df[['name', 'off_season_start', 'off_season_end', 'is_off_season']])