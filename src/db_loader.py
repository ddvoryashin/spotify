import os
import psycopg2
import pandas as pd
import numpy as np
from credentials import *
from psycopg2 import extras


CONN = psycopg2.connect( 
    database =  os.getenv("PG_DATABASE"),
    user =      os.getenv("PG_USERNAME"),
    password =  os.getenv("PG_PASSWORD"),
    host =      os.getenv("PG_HOST"),
    port =      os.getenv("PG_PORT")
)

def insert_values(df: pd.DataFrame, table: str) -> None:
    """
    Insert pandas DataFrame into table
    """

    tuples = [tuple(x) for x in df.to_numpy()]

    cols = ','.join(list(df.columns))
    # SQL query to execute
    query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    print(query)
    cursor = CONN.cursor()
    try:
        extras.execute_values(cursor, query, tuples)
        CONN.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        CONN.rollback()
        cursor.close()
    print(f"Dataframe inserted to {table} table")
    cursor.close()


def execute_query(query: str) -> None:
    """
    Execute query that does not require additional parameters
    """
    cursor = CONN.cursor()
    try:
        cursor.execute(query)
        CONN.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        CONN.rollback()
        cursor.close()
    print("Completed query:")
    print(query)

def merge_values(df: pd.DataFrame, join_field: str, table: str) -> None:
    
    tuples = [tuple(x) for x in df.to_numpy()]
    cols = ','.join(list(df.columns))
    # update fields except for the key
    upd_fields = ""
    for field in df.columns:
        if field != "spotify_id":
            upd_fields = upd_fields + "\t" + field + f" = EXCLUDED.{field},\n"
    # make full query
    # remove new line and comma in the end of upd_fields
    query = f"""
    INSERT INTO {table} ({cols})
    VALUES %s
    ON CONFLICT({join_field})
    DO UPDATE SET
    {upd_fields[:-2]}
    """
    print(query)
    cursor = CONN.cursor()
    try:
        extras.execute_values(cursor, query, tuples)
        CONN.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        CONN.rollback()
        cursor.close()
    print(f"Values merged into {table}")
    cursor.close()
