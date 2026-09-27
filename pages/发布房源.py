import streamlit as st
import folium
from streamlit_folium import st_folium
import random
from analytics import capture_event
import database
from image_service import upload_image_to_cloudinary
from translations import get_translations, translate_value

# Configure page
st.set_page_config(page_title="发布房源", layout="wide")

if "lang" not in st.session_state:
    st.session_state.lang = "zh"

t = get_translations(st.session_state.lang)

# Store selected coordinates in session
if "selected_lat" not in st.session_state:
    st.session_state.selected_lat = -34.9285

if "selected_lng" not in st.session_state:
    st.session_state.selected_lng = 138.6007

with st.sidebar:
    st.page_link("租房地图.py", label=t["nav_map"])
    st.page_link("pages/发布房源.py", label=t["nav_publish"])

st.title(t["publish_title"])
st.page_link("租房地图.py", label=t["publish_back"])

# Input fields
title = st.text_input(t["publish_form_title"])
suburb = st.text_input(t["publish_form_suburb"])
price = st.number_input(t["publish_form_price"], min_value=0)
# 选项值是中文规范值（写进数据库的就是它），format_func 只决定屏幕上显示什么
def format_value(value):
    return translate_value(value, st.session_state.lang)

room_type = st.selectbox(t["publish_form_room_type"], ["单间", "合租", "Studio", "整租"], format_func=format_value)
description = st.text_area(t["publish_form_description"])

uploaded_files = st.file_uploader(t["publish_form_image"], type=["jpg", "png", "jpeg"], accept_multiple_files=True)

contact = st.text_input(t["publish_form_contact"])
phone = st.text_input(t["publish_form_phone"])
wechat = st.text_input(t["publish_form_wechat"])
bill = st.selectbox(t["publish_form_bill"], ["是", "否"], format_func=format_value)
furniture = st.selectbox(t["publish_form_furniture"], ["是", "否"], format_func=format_value)

# Map selection
st.subheader(t["publish_form_location"])

m = folium.Map(
    location=[st.session_state.selected_lat, st.session_state.selected_lng],
    zoom_start=12
)
m.add_child(folium.LatLngPopup())

folium.Marker(
    [st.session_state.selected_lat, st.session_state.selected_lng]
).add_to(m)

map_data = st_folium(m, height=450, use_container_width=True)

if map_data and map_data.get("last_clicked"):
    st.session_state.selected_lat = map_data["last_clicked"]["lat"]
    st.session_state.selected_lng = map_data["last_clicked"]["lng"]
    st.rerun()

latitude = st.number_input(t["publish_form_latitude"], value=st.session_state.selected_lat)
longitude = st.number_input(t["publish_form_longitude"], value=st.session_state.selected_lng)

# Submit
if st.button(t["publish_submit_btn"]):
    if not title.strip():
        st.error(t["publish_error_title"])
    elif price <= 0:
        st.error(t["publish_error_price"])
    else:
        try:
            image_urls = [upload_image_to_cloudinary(f) for f in uploaded_files]
            image_url = ",".join(url for url in image_urls if url)

            database.insert_listing({
                "标题": title,
                "区域": suburb,
                "价格": int(price),
                "房型": room_type,
                "纬度": float(latitude) + random.uniform(-0.0005, 0.0005),
                "经度": float(longitude) + random.uniform(-0.0005, 0.0005),
                "描述": description,
                "图片": image_url,
                "联系人": contact,
                "电话": phone,
                "微信": wechat,
                "是否包bill": bill,
                "是否带家具": furniture,
                "status": "pending"
            })

            st.success(t["publish_success"])
            capture_event("listing_submitted")

        except Exception as e:
            st.error(f"{t['publish_error_upload']}{e}")