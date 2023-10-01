import pandas as pd
import sqlite3

# send dataframe to reviews table in db_steam.db
def send_to_database(df):
    conn = sqlite3.connect('data/db_steam.db')
    df.to_sql('reviews', conn, if_exists='replace', index=False)
    conn.close()

# get dataframe from reviews table in db_steam.db
def get_data_from_database():
    conn = sqlite3.connect('data/db_steam.db')
    df = pd.read_sql('SELECT * FROM reviews', conn)
    conn.close()
    return df
