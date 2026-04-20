import streamlit as st
import os
import uuid
import folium
from streamlit_folium import st_folium

import database

# Configure page
st.set_page_config(page_title="Post Listing", layout="wide")

database.create_table()

# Store selected coordinates in session
if "selected_lat" not in st.session_state:
    st.session_state.selected_lat = -34.9285

if "selected_lng" not in st.session_state:
    st.session_state.selected_lng = 138.6007

st.title("Post a Rental Listing")
st.page_link("app.py", label="← Back to Map")

# Input fields
title = st.text_input("Title")
suburb = st.text_input("Suburb")
price = st.number_input("Price", min_value=0)
room_type = st.selectbox("Room Type", ["Shared", "Single", "Studio", "Entire"])
description = st.text_area("Description")

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

contact = st.text_input("Contact Name")
phone = st.text_input("Phone")
wechat = st.text_input("WeChat")
bill = st.selectbox("Bills Included", ["Yes", "No"])
furniture = st.selectbox("Furnished", ["Yes", "No"])

# Map selection
st.subheader("Select Location on Map")

m = folium.Map(location=[st.session_state.selected_lat, st.session_state.selected_lng], zoom_start=12)
m.add_child(folium.LatLngPopup())

folium.Marker(
    [st.session_state.selected_lat, st.session_state.selected_lng]
).add_to(m)

map_data = st_folium(m, height=450)

if map_data and map_data.get("last_clicked"):
    st.session_state.selected_lat = map_data["last_clicked"]["lat"]
    st.session_state.selected_lng = map_data["last_clicked"]["lng"]
    st.rerun()

latitude = st.number_input("Latitude", value=st.session_state.selected_lat)
longitude = st.number_input("Longitude", value=st.session_state.selected_lng)

# Submit
if st.button("Submit Listing"):

    if uploaded_file is not None:
        os.makedirs("images", exist_ok=True)
        filename = f"{uuid.uuid4().hex}.jpg"
        path = os.path.join("images", filename)

        with open(path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    else:
        path = ""

    database.insert_listing({
        "标题": title,
        "区域": suburb,
        "价格": int(price),
        "房型": room_type,
        "纬度": latitude,
        "经度": longitude,
        "描述": description,
        "图片": path,
        "联系人": contact,
        "电话": phone,
        "微信": wechat,
        "是否包bill": bill,
        "是否带家具": furniture
    })

    st.success("Listing posted successfully!")