import os
import openai
from dotenv import load_dotenv
import snowflake.connector
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine


# Load environment variables from the .env file
load_dotenv()

# Environment Variables
snowflake_account = os.getenv("SNOWFLAKE_ACCOUNT")
snowflake_user = os.getenv("SNOWFLAKE_USER")
snowflake_password = os.getenv("SNOWFLAKE_PASSWORD")
snowflake_database = os.getenv("SNOWFLAKE_DATABASE")
snowflake_table1 = os.getenv("SNOWFLAKE_TABLE1")
snowflake_role = os.getenv("SNOWFLAKE_ROLE")

# Function to establish a connection to Snowflake
def get_snowflake_connection(snowflake_user, snowflake_password, snowflake_account, snowflake_table1, snowflake_database, snowflake_role):
    return snowflake.connector.connect(
        user=snowflake_user,
        password=snowflake_password,
        account=snowflake_account,
        database=snowflake_database,
        table=snowflake_table1,
        role=snowflake_role
    )

# Function to fetch data from Snowflake
def fetch_data(conn, table_name):
    try:
        # SQL query to select data from the table and limit to the first 10 rows
        query = f'SELECT * FROM {table_name} LIMIT 20'

        # Execute the query and fetch data into a Pandas DataFrame
        df = pd.read_sql(query, conn)

        return df

    except Exception as e:
        # If there is an error in the connection or query, return an empty DataFrame
        st.error(f"Error connecting to Snowflake: {str(e)}")
        return pd.DataFrame()

# Establish a connection to Snowflake
snowflake_conn = get_snowflake_connection(snowflake_user, snowflake_password, snowflake_account, snowflake_table1, snowflake_database, snowflake_role)

# Fetch data using the existing connection
df = fetch_data(snowflake_conn, snowflake_table1)

schema = """
CREATE TABLE COVID_WORLDWIDE(
    COUNTRY VARCHAR(16777216),
    TOTAL_CASES NUMBER(38,0),
    CASES_NEW NUMBER(38,0),
    DEATHS NUMBER(38,0),
    DEATHS_NEW NUMBER(38,0),
    TRANSMISSION_CLASSIFICATION VARCHAR(16777216),
    DAYS_SINCE_LAST_REPORTED_CASE NUMBER(38,0),
    COUNTRY_REGION VARCHAR(16777216),
    DATE DATE,
    SITUATION_REPORT_NAME VARCHAR(16777216),
    LAST_UPDATE_DATE TIMESTAMP_NTZ(9),
    LAST_REPORTED_FLAG BOOLEAN,
    MORTALITY NUMBER(18,4),
    CASES_PER_DAY FLOAT,
    MORTALITY_RATE FLOAT,
    HIGH_MORTALITY NUMBER(38,0),
    MONTH NUMBER(38,0),
    NORMALIZED_TOTAL_CASES FLOAT,
    NORMALIZED_DEATHS FLOAT,
    IN_EUROPE BOOLEAN,
    CASES_DEATHS_DIFF NUMBER(38,0),
    CASE_CATEGORY VARCHAR(50),
    ENCODED_TRANSMISSION_CLASSIFICATION NUMBER(38,0)
);
"""

def get_openai_response(question):
    openai.api_key = os.getenv("OPENAI_API")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Given the following SQL table {schema}, your job is to write SQL queries based user's request and process the query on {df} and display both the query and result taken from table);"},
            {"role": "user", "content": f"If the asked question doesn't belong to a SQL query, then tell the user to be specific on what they want to see from the database by displaying the use {schema}. Otherwise, process the SQL query: {question}"},
            {"role": "assistant", "content": f"Run the generated SQL query from user on {df} to fetch the answer from table. Display both the generated query and answer from the table as SQL:\n generated query and Answer:\n result from the table"}
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response['choices'][-1]['message']['content']


def main():
    # Initialize session state to store conversation history
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []

    st.title("OpenAI Chat")

    # Display initial image and text in the center
    st.image("image.jpg", width=75, use_column_width=False, output_format="auto")
    st.write("How can I help you today?") 

    # Get user question
    question = st.chat_input("Your Question")

    if question:
        # Store the user question in the conversation history
        st.session_state.conversation.append(('user', question))

        # Display loading spinner
        with st.spinner("Thinking..."):
            # Get OpenAI response
            answer = get_openai_response(question)

        # Store the OpenAI response in the conversation history
        st.session_state.conversation.append(('openai', answer))

        # Display conversation history
        for role, message in st.session_state.conversation:
            if role == 'user':
                st.write("User:", message)
            elif role == 'openai':
                st.text_area("openai", value=message, key=f"openai_{message}", disabled=True)

if __name__ == "__main__":
    main()