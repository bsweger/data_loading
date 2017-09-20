# Data Loading
Simple Python script for using pandas to load a .csv file to postgres.

This is script is for reference/proof of concept and is not production-ready. At a high level it:

1. Reads a sample .csv into a pandas dataframe.
2. Does some data cleaning.
3. Bulk inserts the clean data into a postgres table.

## Setup

### Postgres

1. Make sure you have access to a Postgres database and credentials that can create tables and insert records.
2. Create the following table in your Postgres database:

```sql
CREATE TABLE "public"."yourtablename" (
    "id" character(36),
    "datecreated" date,
    "username" char(50),
    "first" char(25),
    "last" char(25),
    "email" varchar(50),
    "bio" text,
    "lang" char(2),
    PRIMARY KEY ("id")
);
```

### Python

2. Create a Python virtual environment and activate it.
3. Clone this repo and `cd` into the `data_loading` folder.
4. Install the required Python libraries: `pip install -r requirements.txt`.
5. Rename (or copy) `example_db.cfg` to `db.cfg` and update the information with your postgres hostname, dbname, credentials, and the name of the target table you want load.

## Loading the Data

To load the .csv into Postgres, run the following from the command line:

        python load_csv.py

You should see some console output about the load:

```
INFO:root:Read 10000 rows from data0.csv
INFO:root:Removed 42 duplicate ids from data
INFO:root:Inserted 9958 rows to database
```
