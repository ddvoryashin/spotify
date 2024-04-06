import os
import psycopg2
import pandas as pd
import numpy as np
from credentials import *
from psycopg2 import extras


def insert_values(df: pd.DataFrame, table: str) -> None:

    conn = psycopg2.connect( 
        database =  os.getenv("PG_DATABASE"),
        user =      os.getenv("PG_USERNAME"),
        password =  os.getenv("PG_PASSWORD"),
        host =      os.getenv("PG_HOST"),
        port =      os.getenv("PG_PORT")
    )

    tuples = [tuple(x) for x in df.to_numpy()]

    cols = ','.join(list(df.columns))
    # SQL query to execute
    query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    cursor = conn.cursor()
    try:
        extras.execute_values(cursor, query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        conn.rollback()
        cursor.close()
    print("the dataframe is inserted")
    cursor.close()
