import streamlit as st
import pandas as pd

import data
import filters
import map_view
import ui
import database

# Configure page settings
st.set_page_config(page_title="Adelaide Student Rental Map", layout="wide")

# Ensure database and table exist
database.create_table()

# Initialize database with seed data if empty
conn = database.get_connection()
count = pd.read_sql("SELECT COUNT(*) as count FROM listings", conn).iloc[0]["count"]

if count == 0:
    seed_df = data.get_seed_dataframe()
    seed_df.to_sql("listings", conn, if_exists="append", index=False)

conn.close()

# Page header
st.title("Adelaide Student Rental Map")
st.caption("A map-first rental platform for exploring listings by location and price")

# Navigation to post page
st.page_link("pages/post.py", label="Post Listing", icon="➕")

# Load data from database
df = data.get_dataframe()

# Apply sidebar filters
filtered_df = filters.apply_filters(df)

# Layout: left = list, right = map
col1, col2 = st.columns([1, 2])

with col1:
    ui.render_list(filtered_df)

with col2:
    map_view.render_map(filtered_df)