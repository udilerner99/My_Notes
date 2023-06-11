# Hi,

I'm storing all my tech notes , regarding all sort of topics like git, python, etc...

## New Demo Project
### NYC Taxi drive
In this demo project i'll demonstrate Following procedure:
1. Fetch a sample raw data from https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
2. I'll run profiling on the data and explain how to run initial analyze and understanding of the datasets.
3. Once data source is understood, we can design are Architecture and explain what our data model will look like, data model will be business process driven. https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/business-process/
4. Once our data model is ready, we have a clear view of what data is needed for the project, we can start working on a tool that will fetch the data on regular basis. 
   We'll create a python application, the application will:
        4.1. trigger once a month and download the data into a local path
        4.2. load the data into our database in a raw data format
5. I'll upload the data into a duckDB deployment https://github.com/duckdb/duckdb
6. For demonstrating the customers insights, we want to demonstrate an aggregation table that will represent a report.
    6.1 our report will consist of monthly passengers counts
7. For managing the transformation part of our ELT system, we'll use dbt https://www.getdbt.com/
8. I'll also try to demonstrate an orchestration solution using prefect https://github.com/PrefectHQ/prefect
9. For developing i'll use Visual Studio Code https://code.visualstudio.com/

### Project Structure

    .
    ├── nyc_taxi_demo              # main project folder
    ├──── venv_nyc                    # python virtual environment
    ├──── nyc_data_ingestion_engine   # python application for extracting source data
    ├──── nyc_dbt                     # dbt project for nyc data
    └── README.md