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
    ├──── env_nyc                    # python virtual environment
    ├──── Ingestion   # python application for extracting source data
    ├──── nyc_dbt                     # dbt project for nyc data
    ├──── nyc_taxi_raw_source # landing source data files
    ├──── nyc_taxi_sample_data # sample data for profiling
    └── README.md

## Data Profiling
The purpose of data profiling is to understand the physical data, we want to know the different data sets involve, understand volume sizes, understand the different keys and their uniqueness, understand distinct, max and average length of text and numeric columns.
These columns will be transformed into keys, description and measurement columns of our data model.

### Step 1
1. Download manually a sample file and explore it.
2. looking on our data source, i can see several files per month:
    * Yellow Taxi Trip Records
    * Green Taxi Trip Records
    * For-Hire Vehicle Trip Records
    * High Volume For-Hire Vehicle Trip Records
3. For this project we'll focus only on the Yellow Taxi trip records data, we can see that for each month we have a separate file and link, and the file is in a parquet format.
Parquet file format is a columnar file, which store the data by columns and saving metadata regarding the columns in the physical file, also the format uses compression.
4. Since the parquet format is binary, we can just look on the content like a csv file for example, we need a tool, i've decided to use https://github.com/chhantyal/parquet-cli
    * from this point we need to work in a virtual environment for python
        * create a virtual environment inside your project main folder: python -m venv myenv (you can replace "myenv" with your desired name)
        * i've decided to name it "env_nyc"
        * now we can activate it using source {myenv}/bin/activate
        * i recommend using zsh for cli, and adding the path as an alias.
        * install the parquet-cli tool using pip
        * at this point we'll run : "pip freeze > requirements.txt", in order to create a requirements.txt file so that other users may be also using the project to install locally the required packages for the project
    * lets look on the sample file data by running: parq /nyc_taxi_sample_data/yellow_tripdata_2023-01.parquet
    * we can see following summarize information:
    #### Metadata 
        <pyarrow._parquet.FileMetaData object at 0x1321d8860>
        created_by: parquet-cpp-arrow version 8.0.0
        num_columns: 19
        num_rows: 3066766
        num_row_groups: 1
        format_version: 1.0
        serialized_size: 10386
    * now lets run parq yellow_tripdata_2023-01.parquet --schema
    * we can see the file schema information:
    #### Schema 
    <pyarrow._parquet.ParquetSchema object at 0x1009be200>
    required group field_id=-1 schema {
    optional int64 field_id=-1 VendorID;
    optional int64 field_id=-1 tpep_pickup_datetime (Timestamp(isAdjustedToUTC=false, timeUnit=microseconds, is_from_converted_type=false, force_set_converted_type=false));
    optional int64 field_id=-1 tpep_dropoff_datetime (Timestamp(isAdjustedToUTC=false, timeUnit=microseconds, is_from_converted_type=false, force_set_converted_type=false));
    optional double field_id=-1 passenger_count;
    optional double field_id=-1 trip_distance;
    optional double field_id=-1 RatecodeID;
    optional binary field_id=-1 store_and_fwd_flag (String);
    optional int64 field_id=-1 PULocationID;
    optional int64 field_id=-1 DOLocationID;
    optional int64 field_id=-1 payment_type;
    optional double field_id=-1 fare_amount;
    optional double field_id=-1 extra;
    optional double field_id=-1 mta_tax;
    optional double field_id=-1 tip_amount;
    optional double field_id=-1 tolls_amount;
    optional double field_id=-1 improvement_surcharge;
    optional double field_id=-1 total_amount;
    optional double field_id=-1 congestion_surcharge;
    optional double field_id=-1 airport_fee;
    }
    * now lets check some sample raw data 
parq yellow_tripdata_2023-01.parquet --head 10
   VendorID tpep_pickup_datetime tpep_dropoff_datetime  passenger_count trip_distance  RatecodeID store_and_fwd_flag  PULocationID  DOLocationID
0         2  2023-01-01 00:32:10   2023-01-01 00:40:36              1.0          0.97         1.0                  N           161           141
1         2  2023-01-01 00:55:08   2023-01-01 01:01:27              1.0          1.10         1.0                  N            43           237
2         2  2023-01-01 00:25:04   2023-01-01 00:37:49              1.0          2.51         1.0                  N            48           238
3         1  2023-01-01 00:03:48   2023-01-01 00:13:25              0.0          1.90         1.0                  N           138             7
4         2  2023-01-01 00:10:29   2023-01-01 00:21:19              1.0          1.43         1.0                  N           107            79
5         2  2023-01-01 00:50:34   2023-01-01 01:02:52              1.0          1.84         1.0                  N           161           137
6         2  2023-01-01 00:09:22   2023-01-01 00:19:49              1.0          1.66         1.0                  N           239           143
7         2  2023-01-01 00:27:12   2023-01-01 00:49:56              1.0         11.70         1.0                  N           142           200
8         2  2023-01-01 00:21:44   2023-01-01 00:36:40              1.0          2.95         1.0                  N           164           236
9         2  2023-01-01 00:39:42   2023-01-01 00:50:36              1.0          3.01         1.0                  N           141           107

   payment_type  fare_amount  extra  mta_tax  tip_amount  tolls_amount improvement_surcharge  total_amount  congestion_surcharge  airport_fee
0             2          9.3   1.00      0.5        0.00           0.0                   1.0         14.30                   2.5         0.00
1             1          7.9   1.00      0.5        4.00           0.0                   1.0         16.90                   2.5         0.00
2             1         14.9   1.00      0.5       15.00           0.0                   1.0         34.90                   2.5         0.00
3             1         12.1   7.25      0.5        0.00           0.0                   1.0         20.85                   0.0         1.25
4             1         11.4   1.00      0.5        3.28           0.0                   1.0         19.68                   2.5         0.00
5             1         12.8   1.00      0.5       10.00           0.0                   1.0         27.80                   2.5         0.00
6             1         12.1   1.00      0.5        3.42           0.0                   1.0         20.52                   2.5         0.00
7             1         45.7   1.00      0.5       10.74           3.0                   1.0         64.44                   2.5         0.00
8             1         17.7   1.00      0.5        5.68           0.0                   1.0         28.38                   2.5         0.00
9             2         14.9   1.00      0.5        0.00           0.0                   1.0         19.90                   2.5         0.00
    * we can gain from the profiling following insights:
    - we have 2 main dates: tpep_pickup_datetime & tpep_dropoff_datetime, for our model we'll focus on the pickup datetime which will represent the date when the passenger was picked.
    - we have the following measure : field passenger_count, trip_distance, fare_amount, tip_amount, tolls_amount, mta_tax, extra, total_amount, airport_fee.
    - we don't have any description fields, but we do have several fields that seems to be keys for the type of data : VendorID, RatecodeID,PULocationID, DOLocationID, payment_type
    - I have decided to use a simple star schema design following kimball methodology (https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/star-schema-olap-cube/)
    - looking on the dataset we can see immediately that we have a single fact table which represent a business process of a taxi trip for passengers.
    - our fact grain is: PULocationID, DOLocationID, VendorID, VendorID, RatecodeID, store_and_fwd_flag,payment_type
    - since we don't have any description for any of the ID fields all will behave as degenerate dimensions, payment_type & store_and_fwd_flag are indication relate to the physical transaction
    - measure that will be derive from the fact are: passenger_count, trip_distance & total_amount
    - Architecture: /nyc_taxi_demo/nyc-architecture.jpg

### Step 2
Lets create the python code for the ingestion engine.
1. The engine needs to iterate over links for the NYC taxi data files, from 2009 till 2023 and download the parquet files into the nyc_taxi_demo/nyc_taxi_raw_source folder.
2. For the script to run make sure to run: pip install requests
3. Don't forget to change the "folder_path" parameter to your local desired path
4. lets run the script, you'll be able to see the downloaded files message for each file, example:
    python Ingestion_engine.py

Downloaded: yellow_tripdata_2009-01.parquet
Downloaded: yellow_tripdata_2009-03.parquet

Great ! we have all the data files !

### Step 3
Lets get busy with the database that will serve us, i could of work with Apache spark, but i wanted to demonstrate a  data pipeline process.
Our Architecture will consist of following data layers (schemas):
1. raw_stage: raw data files, run cleansing/convention naming/casting/null handling.
2. warehouse: confirmed star schema layer (dimensions/atomic granularity facts)
3. mart: bi facing format table, will consist of bwt/aggregated facts for bi purposes

#### Lets set the database
1. install duckDB: brew install duckdb 
2. that's it ! , we can test our instance:
   duckdb                                                                                               
v0.8.0 e8e4cea5ec
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database.
3. now, i'll create a persist table named: source_nyc_yellow_t, which will load all of the source data files.
CREATE TABLE source_nyc_yellow_t as SELECT * FROM read_parquet(['/Users/udilerner/prsnl_projects/My_Notes/nyc_taxi_demo/nyc_taxi_raw_source/*.parquet'], union_by_name=True, filename=true) ;
4. lets sample the table: select * from source_nyc_yellow_t limit 5;
┌──────────┬──────────────────────┬──────────────────────┬─────────────────┬───────────────┬───┬───────────────────┬──────────────────┬───────────────────┬──────────────────────┐
│ VendorID │ tpep_pickup_datetime │ tpep_dropoff_datet…  │ passenger_count │ trip_distance │ … │ dropoff_longitude │ dropoff_latitude │ __index_level_0__ │       filename       │
│  int64   │      timestamp       │      timestamp       │     double      │    double     │   │      double       │      double      │       int64       │       varchar        │
├──────────┼──────────────────────┼──────────────────────┼─────────────────┼───────────────┼───┼───────────────────┼──────────────────┼───────────────────┼──────────────────────┤
│        2 │ 2011-07-01 00:25:00  │ 2011-07-01 00:33:00  │             5.0 │           2.3 │ … │                   │                  │                   │ /Users/udilerner/p…  │
│        2 │ 2011-07-01 00:18:00  │ 2011-07-01 00:20:00  │             5.0 │          0.65 │ … │                   │                  │                   │ /Users/udilerner/p…  │
│        2 │ 2011-07-01 00:22:00  │ 2011-07-01 00:38:00  │             5.0 │          4.51 │ … │                   │                  │                   │ /Users/udilerner/p…  │
│        2 │ 2011-07-01 00:51:00  │ 2011-07-01 00:55:00  │             5.0 │          1.17 │ … │                   │                  │                   │ /Users/udilerner/p…  │
│        1 │ 2011-07-01 00:24:58  │ 2011-07-01 00:29:45  │             2.0 │           1.2 │ … │                   │                  │                   │ /Users/udilerner/p…  │
├──────────┴──────────────────────┴──────────────────────┴─────────────────┴───────────────┴───┴───────────────────┴──────────────────┴───────────────────┴──────────────────────┤
│ 5 rows                                                                                                                                                    42 columns (9 shown) │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

5. we can see that there are columns not shown on our original schema from the latest file, probably changes had been made in the last years. for simplicity purposes we'll create a table that will aggregate the passengers count by month.

create table f_nyc_yellow_agg as SELECT strftime(tpep_pickup_datetime, '%Y/%m') as dt_year_month,sum(passenger_count) as msr_count_pssngr from source_nyc_yellow_t where tpep_pickup_datetime <='2023-03-01' group by 1 order by 1 asc;
┌───────────────┬──────────────────┐
│ dt_year_month │ msr_count_pssngr │
│    varchar    │      double      │
├───────────────┼──────────────────┤
│ 2022/06       │        4792144.0 │
│ 2022/07       │        4386947.0 │
│ 2022/08       │        4353905.0 │
│ 2022/09       │        4252079.0 │
│ 2022/10       │        4905091.0 │
│ 2022/11       │        4360904.0 │
│ 2022/12       │        4646436.0 │
│ 2023/01       │        4080782.0 │
│ 2023/02       │        3838267.0 │
│ 2023/03       │              4.0 │
├───────────────┴──────────────────┤
│ 160 rows (40 shown)    2 columns │
└──────────────────────────────────┘

### Step 4
For demonstration of working with dbt, i've decided to use a snowflake account, setting a free account is easy and it will grant you 30 free days of usage.

#### set the database
1. i'll use the db_init.sql script to manage the snowflake database.
2. once database and schemas lets create the source table on raw_src schema.
    (Can be found on the nyc_yellow_taxi_t)
3. using snowflake interface we can quickly upload files into tables, ofcourse we could also use cli command to copy the data.
4. now that we have a snowflake database with base schema and source table ready , lets create the dbt project.
    just create a new folder to store the dbt project files, and run dbt init (assuming you have dbt installed)
that's it we are ready, we can check connection :
dbt debug                                                                                                                  ✔  env_nyc  
08:43:34  Running with dbt=1.5.0
08:43:34  dbt version: 1.5.0
08:43:34  python version: 3.10.4
08:43:34  python path: /Users/udilerner/.pyenv/versions/3.10.4/bin/python
08:43:34  os info: macOS-13.4-arm64-arm-64bit
08:43:34  Using profiles.yml file at /Users/udilerner/.dbt/profiles.yml
08:43:34  Using dbt_project.yml file at /Users/udilerner/prsnl_projects/My_Notes/nyc_taxi_demo/nyc_taxi_dbt/dbt_project.yml
08:43:34  Configuration:
08:43:35    profiles.yml file [OK found and valid]
08:43:35    dbt_project.yml file [OK found and valid]
08:43:35  Required dependencies:
08:43:35   - git [OK found]

08:43:35  Connection:
08:43:35    account: mob96890
08:43:35    user: udilr
08:43:35    database: taxi_data
08:43:35    schema: raw_stage
08:43:35    warehouse: compute_wh
08:43:35    role: accountadmin
08:43:35    client_session_keep_alive: False
08:43:35    query_tag: None
08:43:37    Connection test: [OK connection ok]

08:43:37  All checks passed!

when working in vs code i recommend using the snowflake extension and dbt power user extension.

5. now that we connected with dbt we can start write our models.
6. lets start with defining our source metadata on the sources_metadata.yml file.
using get_ddl we can get source table schema for the metadata creation:

select get_ddl('table','TAXI_DATA.RAW_SRC.RAW_NYC_YELLOW_TAXI_T');

create or replace TABLE RAW_NYC_YELLOW_TAXI_T (
	VENDORID NUMBER(38,0),
	TPEP_PICKUP_DATETIME TIMESTAMP_NTZ(9),
	TPEP_DROPOFF_DATETIME TIMESTAMP_NTZ(9),
	PASSENGER_COUNT NUMBER(38,0),
	TRIP_DISTANCE NUMBER(38,0),
	RATECODEID NUMBER(38,0),
	STORE_AND_FWD_FLAG VARCHAR(16777216),
	PULOCATIONID NUMBER(38,0),
	DOLOCATIONID NUMBER(38,0),
	PAYMENT_TYPE NUMBER(38,0),
	FARE_AMOUNT FLOAT,
	EXTRA FLOAT,
	MTA_TAX FLOAT,
	TIP_AMOUNT FLOAT,
	TOLLS_AMOUNT FLOAT,
	IMPROVEMENT_SURCHARGE FLOAT,
	TOTAL_AMOUNT FLOAT,
	CONGESTION_SURCHARGE FLOAT,
	AIRPORT_FEE FLOAT
);
7. lets start with a model on the raw_stage to clean/confirm and cast our table columns.
this model will materialize as a view.

At this point it's also worth mentioning that i've added an fk_audit column, this will help us trace the job that loaded the records.
 '{{ invocation_id }}' as fk_audit


8. now that we have raw_stage view ready, lets move on to the staging layer.
usually this layer will serve as layer to connect different source tables and join them into confirmed dimensions or fact tables.

in our case we'll have one fact table, the id's as mentioned will serve as degenerate dimensions.

9. moving to the fact table, we assume that the source is behaving as a classic transactional event table, each record represent a new "event" in our case a taxi driver picked up a passenger and then drop him off, and that's the "end of life" for the transaction.

assuming this we can materialize the fact table as incremental and filtering on new records only using the dates columns.

once we run the fact table lets count the number of records:

select
count(*)
from warehouse.f_taxi_rides_t;
3066766

now lets try to rerun the build of the fact table but this time without the -full-refresh flag for incremental load only, we expect the the number of records will remain the same.

and it does!
10. lets create an aggregated table for daily reports.
we want to count each day the summarize of the rides amount & passenger count.

11. also added metadata file for the fact with tests of not_null

### Step 5
lets change the ingestion engine to run in a multi thread environment in order to download the source files more efficiently.

we can utilize Python's concurrent.futures module, which provides a high-level interface for asynchronously executing functions.

The script uses a ThreadPoolExecutor to manage a pool of worker threads. It iterates over the months and years, constructs the URL for each month, and submits the download task to the executor asynchronously using executor.submit(). This allows the files to be downloaded in parallel.

After submitting all tasks, the script waits for all tasks to complete by calling executor.shutdown(wait=True). This ensures that the script does not exit before all downloads are finished.