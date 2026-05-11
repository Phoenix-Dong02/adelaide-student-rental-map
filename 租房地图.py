import streamlit as st
from analytics import capture_event
import data
import filters
import map_view
import ui
import database
from translations import get_translations

st.set_page_config(
    page_title="阿德莱德租房地图",
    layout="wide",
    initial_sidebar_state="expanded"
)


hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stSidebarNavLink"][href$="/admin"] {display: none;}
    [data-testid="stSidebarNavLink"][href$="/dashboard"] {display: none;}
    [data-testid="stToolbar"] {visibility: hidden;}
    [data-testid="stSidebarCollapsedControl"] {visibility: visible;}
    </style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

if "lang" not in st.session_state:
    st.session_state.lang = "zh"

is_owner = st.query_params.get("owner") == st.secrets.get("OWNER_TOKEN")

if "visit_recorded" not in st.session_state and not is_owner:
    database.record_page_visit()
    capture_event("page_view")
    st.session_state.visit_recorded = True

t = get_translations(st.session_state.lang)

col1, col2 = st.columns([15, 1])
with col1:
    st.title(t["main_title"])
with col2:
    lang_btn = t["english_btn"] if st.session_state.lang == "zh" else t["chinese_btn"]
    if st.button(lang_btn, key="lang_toggle"):
        st.session_state.lang = "en" if st.session_state.lang == "zh" else "zh"
        st.rerun()

st.caption(t["main_subtitle"])


df = data.get_dataframe()
filtered_df = filters.apply_filters(df, t)

if "selected_listing_id" not in st.session_state:
    st.session_state.selected_listing_id = None

if "listing_id" in st.query_params:
    st.session_state.selected_listing_id = int(st.query_params["listing_id"])

col1, col2 = st.columns([1.1, 4.2])

with col2:
    clicked_id = map_view.render_map(filtered_df, t)

if clicked_id is not None:
    st.session_state.selected_listing_id = clicked_id

with col1:
    ui.render_selected_listing(filtered_df, t)

with st.sidebar:
    st.divider()
    st.subheader(t["feedback_header"])

    feedback = st.text_area(t["feedback_prompt"])

    if st.button(t["feedback_submit_btn"]):
        if feedback.strip():
            database.insert_feedback(feedback.strip())
            capture_event("feedback_submitted")
            st.success(t["feedback_success"])