import pandas as pd
import database


def get_seed_dataframe():
    listings = []
    return pd.DataFrame(listings)


def get_dataframe():
    return database.get_active_listings()