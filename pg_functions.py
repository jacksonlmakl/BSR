import pandas as pd
import numpy as np
from sqlalchemy import create_engine,text
import psycopg2

def pg_connection():
    # PostgreSQL connection details
    username = 'georgetown'
    password = 'georgetown123'
    host = 'ls-e8ed76a5368bcf40d7d7a6e7de5bca06d7ceca3b.cx6iawau684h.us-east-1.rds.amazonaws.com'
    port = '5432'
    database = 'BSR'  # Replace with your actual database name
    
    # Create connection string
    connection_string = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}'
    
    conn=create_engine(connection_string).connect()
    return conn
    
def sql(query):
    # Example of executing a SQL query to create a new table
    conn=pg_connection()
    r=conn.execute(text(query))
    if r.returns_rows:
        keys=list(r.keys())
        rows=r.all()
        data=[dict(zip(keys,i)) for i in rows]
        return pd.DataFrame(data)
    else:
        return r


def excel_to_table(file_path,sheet_name,schema,table_name):

    df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    # Create engine
    engine = pg_connection().engine
    
    
    # Write the DataFrame to PostgreSQL, specifying the schema
    df.to_sql(table_name, engine, schema=schema, if_exists='replace', index=False)
    
    print("Data successfully written to the ANALYSIS schema in PostgreSQL")
    return df


def df_to_table(df,schema,table_name):

    # Create engine
    engine = pg_connection().engine
    
    # Write the DataFrame to PostgreSQL, specifying the schema
    df.to_sql(table_name, engine, schema=schema, if_exists='replace', index=False)
    
    print("Data successfully written to the ANALYSIS schema in PostgreSQL")
    df.to_csv(f"{table_name}.csv")
    return df