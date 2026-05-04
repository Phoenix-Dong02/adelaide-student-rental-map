import streamlit as st

import data
import filters
import map_view
import ui
import database

st.set_page_config(
    page_title="阿德莱德租房地图",
    layout="wide",
    initial_sidebar_state="expanded"
)


hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

if "visit_recorded" not in st.session_state:
    database.record_page_visit()
    st.session_state.visit_recorded = True

st.title("阿德莱德租房地图")
st.caption("以地图为核心，更直观地按位置和价格找房")


df = data.get_dataframe()
filtered_df = filters.apply_filters(df)

if "selected_listing_id" not in st.session_state:
    st.session_state.selected_listing_id = None

if "listing_id" in st.query_params:
    st.session_state.selected_listing_id = int(st.query_params["listing_id"])

col1, col2 = st.columns([1.1, 4.2])

with col2:
    clicked_id = map_view.render_map(filtered_df)

if clicked_id is not None:
    st.session_state.selected_listing_id = clicked_id

with col1:
    ui.render_selected_listing(filtered_df)

with st.sidebar:
    st.divider()
    st.subheader("意见反馈")

    feedback = st.text_area("你有什么建议？")

    if st.button("提交反馈"):
        if feedback.strip():
            database.insert_feedback(feedback.strip())
            st.success("感谢你的反馈！")