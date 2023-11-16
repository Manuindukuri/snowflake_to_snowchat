from snowflake.snowpark import Session
import snowflake.snowpark.functions as F

def create_covid_data_view(session):
    session.use_schema('ANALYTICS')

    # Define the tables
    nyc = session.table("COVID_NYC.CLEANED_NYC_HEALTH_TESTS").select(
        F.col("MODIFIED_ZCTA"),
        F.col("COVID_CASE_COUNT"),
        F.col("TOTAL_COVID_TESTS"),
        F.col("PERCENT_POSITIVE"),
        F.col("DATE"),
        F.col("FIPS"),
        F.col("COUNTRY_REGION"),
        F.col("ISO3166_1"),
        F.col("ISO3166_2"),
        F.col("LAST_UPDATED_DATE"),
        F.col("LAST_REPORTED_DATE")
    )

    reports = session.table("COVID_WORLDWIDE.CLEANED_WORLD_HEALTH_TESTS").select(
        F.col("COUNTRY"),
        F.col("TOTAL_CASES"),
        F.col("CASES_NEW"),
        F.col("DEATHS"),
        F.col("DEATHS_NEW"),
        F.col("TRANSMISSION_CLASSIFICATION"),
        F.col("DAYS_SINCE_LAST_REPORTED_CASE"),
        F.col("COUNTRY_REGION"),
        F.col("DATE"),
        F.col("SITUATION_REPORT_NAME"),
        F.col("LAST_UPDATE_DATE"),
        F.col("LAST_REPORTED_FLAG"),
        F.col("MORTALITY")
    )

    # Perform the join
    joined_df = nyc.join(
        reports,
        nyc['COUNTRY_REGION'] == reports['COUNTRY_REGION'],
        rsuffix='_r'
    )

    # Continue with additional steps or transformations if needed
    # ...

    # Optionally, you can create or replace a view with the result
    joined_df.create_or_replace_view('JOINED_COVID_DATA_VIEW')

    # Additional steps, if any
    # ...

# For local debugging
if __name__ == "__main__":
    import os, sys
    current_dir = os.getcwd()
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)

    from utils import snowpark_utils
    session = snowpark_utils.get_snowpark_session()

    create_covid_data_view(session)

    session.close()

