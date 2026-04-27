import streamlit as st

import data
import filters
import map_view
import ui
import database

st.set_page_config(page_title="阿德莱德学生租房地图", layout="wide")

database.create_table()
database.migrate_database()
database.create_tracking_tables()

if "visit_recorded" not in st.session_state:
    database.record_page_visit()
    st.session_state.visit_recorded = True

st.title("阿德莱德学生租房地图")
st.caption("以地图为核心，更直观地按位置和价格找房")

st.page_link("pages/发布房源.py", label="管理员发布", icon="➕")

df = data.get_dataframe()

filtered_df = filters.apply_filters(df)

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
        database.insert_feedback(feedback.strip())
        st.success("感谢你的反馈！")