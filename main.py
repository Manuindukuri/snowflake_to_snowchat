import os
import logging
from dotenv import load_dotenv
import snowflake.connector
import pandas as pd
import streamlit as st

# Load environment variables from the .env file
load_dotenv()

# Log metrics
logging.basicConfig(level=logging.INFO)

# Environment Variables
snowflake_account = os.getenv("SNOWFLAKE_ACCOUNT")
snowflake_user = os.getenv("SNOWFLAKE_USER")
snowflake_password = os.getenv("SNOWFLAKE_PASSWORD")
snowflake_database = os.getenv("SNOWFLAKE_DATABASE")
snowflake_table = os.getenv("SNOWFLAKE_TABLE")
snowflake_role = os.getenv("SNOWFLAKE_ROLE")


@st.cache_data
def fetch_data():
    try:
        # Connect to Snowflake
        conn = snowflake.connector.connect(
            user=snowflake_user,
            password=snowflake_password,
            account=snowflake_account,
            database=snowflake_database,
            role=snowflake_role
        )

        # Specify the table name you want to fetch
        table_name = snowflake_table

        # SQL query to select data from the table and limit to the first 10 rows
        query = f'SELECT * FROM {table_name} LIMIT 10'

        # Execute the query and fetch data into a Pandas DataFrame
        df = pd.read_sql(query, conn)

        # Close the Snowflake connection
        conn.close()

        return df

    except Exception as e:
        # If there is an error in the connection or query, return an empty DataFrame
        st.error(f"Error connecting to Snowflake: {str(e)}")
        return pd.DataFrame()

st.title("Display Data from Snowflake in Streamlit")

data = fetch_data()

if not data.empty:
    st.write("First 10 rows of the table:")
    st.dataframe(data)

