import os
from dotenv import load_dotenv
import snowflake.connector
import pandas as pd
import streamlit as st

# Load environment variables from the .env file
load_dotenv()

# Environment Variables
snowflake_account = os.getenv("SNOWFLAKE_ACCOUNT")
snowflake_user = os.getenv("SNOWFLAKE_USER")
snowflake_password = os.getenv("SNOWFLAKE_PASSWORD")
snowflake_database = os.getenv("SNOWFLAKE_DATABASE")
snowflake_table1 = os.getenv("SNOWFLAKE_TABLE1")
snowflake_table2 = os.getenv("SNOWFLAKE_TABLE2")
snowflake_table3 = os.getenv("SNOWFLAKE_TABLE3")
snowflake_role = os.getenv("SNOWFLAKE_ROLE")

# Define a list of table names from your environment variables
tables = [
    snowflake_table1,
    snowflake_table2,
    snowflake_table3
]

@st.cache_data
def fetch_data(table_name):
    try:
        # Connect to Snowflake
        conn = snowflake.connector.connect(
            user=snowflake_user,
            password=snowflake_password,
            account=snowflake_account,
            database=snowflake_database,
            role=snowflake_role
        )

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

st.title("Snowflake Data")

def pandas_table():
    for table in tables:
        data = fetch_data(table)
        if not data.empty:
            st.subheader(f"First 10 rows of the table {table}")
            st.dataframe(data)
            # Assuming you have a DataFrame 'data'
            data = pd.DataFrame({
                'Unique':data.nunique(),
                'Null':data.isnull().sum(),
                'NullPercent':data.isnull().sum() / len(data),
                'NaNN':data.isna().sum(),
                'Type':data.dtypes.values
            })

            # Display the DataFrame with a custom message
            st.write(f"The Schema of the table {table}")
            st.table(data)

pandas_table()