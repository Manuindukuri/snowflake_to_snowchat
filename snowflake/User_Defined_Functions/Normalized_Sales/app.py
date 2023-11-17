import os
from dotenv import load_dotenv
import snowflake.connector 
import configparser
import sys

load_dotenv()

def calculate_normalized_sales(sales_amount, total_cases):
    if total_cases > 0:
        normalized_sales = sales_amount / total_cases
    else:
        normalized_sales = 0
    return normalized_sales

def fetch_data_for_country(country_name):
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

        # Build the query based on the user input
        query = f"SELECT * FROM HOL_DB1.ANALYTICS.NORMALIZED_SALES WHERE COUNTRY_REGION = '{country_name}' limit 1"
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

    # Process the data and calculate normalized sales
    for row in data_for_country:
        country_region = row[0]
        date = row[1]
        total_cases = row[2]
        retailer = row[3]
        sales_amount = row[4]
        product = row[5]

        normalized_sales = calculate_normalized_sales(sales_amount, total_cases)

        print(f"Country Region: {country_region}, Date: {date}, Retailer: {retailer}, Normalized Sales: {normalized_sales}")
