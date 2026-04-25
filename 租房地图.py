import streamlit as st
import pandas as pd

import data
import filters
import map_view
import ui
import database


database.create_tracking_tables()

conn = database.get_connection()
conn.execute("INSERT INTO page_visits DEFAULT VALUES")
conn.commit()
conn.close()

# Configure page settings
st.set_page_config(page_title="阿德莱德学生租房地图", layout="wide")

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
st.title("阿德莱德学生租房地图")
st.caption("以地图为核心，更直观地按位置和价格找房")

# Navigation to post page
st.page_link("pages/发布房源.py", label="发布房源", icon="➕")

# Load data from database
df = data.get_dataframe()

# Apply sidebar filters
filtered_df = filters.apply_filters(df)

# Layout: left = list, right = map
col1, col2 = st.columns([0.8, 4.2])

with col1:
    ui.render_list(filtered_df)

with col2:
    map_view.render_map(filtered_df)

st.divider()
st.subheader("意见反馈")

feedback = st.text_area("你有什么建议？")

if st.button("提交反馈"):
    if feedback.strip():
        conn = database.get_connection()
        conn.execute(
            "INSERT INTO feedback (content) VALUES (?)",
            (feedback,)
        )
        conn.commit()
        conn.close()
        st.success("感谢你的反馈！")