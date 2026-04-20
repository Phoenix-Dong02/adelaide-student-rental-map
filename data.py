import pandas as pd
import sqlite3

def get_seed_dataframe():
    # Initial sample listings used when database is empty
    listings = [
        # Sample data entries (can be replaced with real data later)
    ]
    return pd.DataFrame(listings)


def get_dataframe():
    # Load all listings from SQLite database
    conn = sqlite3.connect("rent.db")
    df = pd.read_sql("SELECT * FROM listings", conn)
    conn.close()
    return df