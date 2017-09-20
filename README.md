# Data Loading
Simple Python script for using pandas to load a .csv file to postgres.

This is script is for reference/proof of concept and is not production-ready. At a high level it:

1. Reads a sample .csv into a pandas dataframe.
2. Does some data cleaning.
3. Bulk inserts the clean data into a postgres table.

## Setup

1. Make sure you have access to a Postgres database and credentials that can create tables and insert records.
2. Create a Python virtual environment and activate it.
3. Clone this repo and `cd` into the `data_loading` folder.
4. Install the required Python libraries: `pip install -r requirements.txt`.
5. Rename (or copy) `example_db.cfg` to `db.cfg` and update the information with your postgres hostname, dbname, credentials, and the name of the target table you want load.
