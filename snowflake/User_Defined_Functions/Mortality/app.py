import os
from dotenv import load_dotenv
import snowflake.connector
import configparser

load_dotenv()

def calculate_mortality_rate(total_cases, deaths):
    if total_cases > 0:
        mortality_rate = (deaths / total_cases) * 100
    else:
        mortality_rate = 0
    return mortality_rate

def fetch_data_for_country(country_name):
    # Read Snowflake credentials from the ~/.snowsql/config file
    snowflake_config = configparser.ConfigParser()
    snowflake_config.read(os.path.expanduser("~/.snowsql/config"))

    # Replace these placeholders with the actual section and option names from your config file
    user = snowflake_config.get("connections.dev", "username")
    password = snowflake_config.get("connections.dev", "password")
    account = snowflake_config.get("connections.dev", "accountname")
    warehouse = snowflake_config.get("connections.dev", "warehousename")
    database = snowflake_config.get("connections.dev", "dbname")
    schema = snowflake_config.get("connections.dev", "rolename")

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

        # Build the query based on the user input
        query = f"SELECT * FROM HOL_DB1.ANALYTICS.COVID_WORLDWIDE_VIEW WHERE COUNTRY = '{country_name}' limit 1"
        cursor.execute(query)

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        return rows

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

if __name__ == "__main__":
    # Allow the user to input the country name
    country_name = input("Enter the country name: ")

    # Fetch data from the view for the specified country
    data_for_country = fetch_data_for_country(country_name)

    # Process the data and calculate mortality rate
    for row in data_for_country:
        country = row[0]
        total_cases = row[1]
        deaths = row[2]

        mortality_rate = calculate_mortality_rate(total_cases, deaths)

        print(f"Country: {country}, Mortality Rate: {mortality_rate}%")
