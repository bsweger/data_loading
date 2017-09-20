import configparser
import logging

import numpy as np
import pandas as pd
from sqlalchemy import create_engine


def load_csv(file_location):
    """Load a .csv into a pre-existing postgres table."""

    # TODO: more robust logging setup and execution
    logging.basicConfig(level=logging.INFO)

    # get db credentials and connection info from config file
    config = configparser.ConfigParser()
    config.read('db.cfg')
    postgres = config['postgres']
    target_table = postgres['table']

    # create database engine and connection
    uri = get_postgres_uri(postgres)
    engine = create_engine(uri)
    connection = engine.connect()

    data = pd.read_csv(file_location, encoding='latin_1')
    logging.info('Read {} rows from {}'.format(len(data), file_location))
    data = clean_data(data)

    # make this script re-runnable by first deleting existing records from db
    sql = 'delete from {}'.format(target_table)
    engine.execute(sql)
    # bulk insert dataframe contents
    data.to_sql(target_table, connection, if_exists='append', index=False)

    # check rowcount of the target table
    # TODO: raise error if db rowcount doesn't match number of dataframe rows
    sql = 'select count(*) from {}'.format(target_table)
    db_rows = engine.execute(sql).scalar()
    logging.info('Inserted {} rows to database'.format(db_rows))


def clean_data(data):
    """Return a clean copy of the dataset."""

    # Update 'null' strings' to empty values in the lang column
    data.lang.replace(r'(?i)null', np.nan, inplace=True, regex=True)

    # Update 'null' strings to empty values in the date column
    data.datecreated.replace(r'(?i)null', np.nan, inplace=True, regex=True)

    # Remove duplicate id (keep the first one)
    original_rowcount = len(data)
    data.drop_duplicates(subset='id', inplace=True)
    logging.info('Removed {} duplicate ids from data'.format(
        original_rowcount - len(data)))

    return data


def get_postgres_uri(postgres):
    """Returns a postgres connection URI."""

    # TODO: add some error checking of config file values
    # TODO: consider setting an environment variable with the uri string instead
    user = postgres.get('user')
    password = postgres.get('password')
    host = postgres.get('host', 'localhost')
    port = postgres.get('port', 5432)
    dbname = postgres.get('dbname', 'postgres')

    return 'postgresql://{}:{}@{}:{}/{}'.format(
        user, password, host, port, dbname
    )


if __name__ == '__main__':
    # TODO: don't hardcode the filename
    load_csv('data0.csv')
