import os
from dotenv import load_dotenv
import snowflake.connector 
import configparser
import sys

load_dotenv()

def calculate_vaccination_rate(total_vaccinations, avg_daily_vaccinations):
    if avg_daily_vaccinations > 0:
        vaccination_rate = (total_vaccinations / avg_daily_vaccinations)
    else:
        vaccination_rate = 0
    return vaccination_rate

def fetch_data_from_view(country_filter=None):
    user = os.getenv("username")
    password = os.getenv("password")
    account = os.getenv("accountname")
    warehouse = os.getenv("warehousename")
    database = os.getenv("dbname")
    schema = os.getenv("rolename")  # Assuming schema is specified in the rolename field

    # Connect to Snowflake using stored credentials
    connection = snowflake.connector.connect(
        user=user,
        password=password,
        account=account,
        warehouse=warehouse,
        database=database,
        schema=schema
    )

    try:
        # Create a cursor object
        cursor = connection.cursor()

        # Build the query based on whether a country filter is provided
        if country_filter:
            query = f"SELECT * FROM HOL_DB1.ANALYTICS.COVID_VACCINATIONS_VIEW WHERE COUNTRY_REGION = '{country_filter}'"
        else:
            query = "SELECT * FROM HOL_DB1.ANALYTICS.COVID_VACCINATIONS_VIEW"

        # Execute the query to fetch data from the view
        cursor.execute(query)

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        return rows

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

if __name__ == "__main__":
    # Allow the user to input the country region
    country_filter = input("Enter the country region: ")

    # Fetch data from the view with or without the country filter
    data_from_view = fetch_data_from_view(country_filter)

    # Process the data and calculate vaccination rate
    for row in data_from_view:
        year = row[0]
        month = row[1]
        country = row[2]
        total_vaccinations = row[3]
        avg_daily_vaccinations = row[4]

        vaccination_rate = calculate_vaccination_rate(total_vaccinations, avg_daily_vaccinations)

        print(f"Year: {year}, Month: {month}, Country: {country}, Vaccination Rate: {vaccination_rate}")
