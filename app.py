import data
import filters
import map_view
import ui
import streamlit as st

st.set_page_config(page_title="阿德莱德留学生租房地图", layout="wide")

df = data.get_dataframe()
filtered_df = filters.apply_filters(df)

col1, col2 = st.columns([1, 2])

with col1:
    ui.render_list(filtered_df)

with col2:
    map_view.render_map(filtered_df)

