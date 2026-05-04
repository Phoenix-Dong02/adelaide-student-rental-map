import streamlit as st
import folium
from streamlit_folium import st_folium
import random

import database
from image_service import upload_image_to_cloudinary

# Configure page
st.set_page_config(page_title="发布房源", layout="wide")

database.create_table()

# Store selected coordinates in session
if "selected_lat" not in st.session_state:
    st.session_state.selected_lat = -34.9285

if "selected_lng" not in st.session_state:
    st.session_state.selected_lng = 138.6007

st.title("发布房源")

password = st.text_input("管理员密码", type="password")

if password != st.secrets.get("ADMIN_PASSWORD"):
    st.warning("请输入管理员密码后发布房源。")
    st.stop()
st.page_link("租房地图.py", label="← 返回地图")

# Input fields
title = st.text_input("标题")
suburb = st.text_input("区域")
price = st.number_input("价格（澳元/周）", min_value=0)
room_type = st.selectbox("房型", ["单间", "合租", "Studio", "整租"])
description = st.text_area("描述")

uploaded_file = st.file_uploader("上传图片", type=["jpg", "png", "jpeg"])

contact = st.text_input("联系人")
phone = st.text_input("电话")
wechat = st.text_input("微信")
bill = st.selectbox("是否包 bill", ["是", "否"])
furniture = st.selectbox("是否带家具", ["是", "否"])

# Map selection
st.subheader("在地图上选择位置")

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

latitude = st.number_input("纬度", value=st.session_state.selected_lat)
longitude = st.number_input("经度", value=st.session_state.selected_lng)

# Submit
if st.button("提交房源"):
    if not title.strip():
        st.error("标题不能为空。")
    elif price <= 0:
        st.error("价格必须大于 0。")
    else:
        try:
            image_url = upload_image_to_cloudinary(uploaded_file)

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
                "status": "active" 
            })

            st.success("房源发布成功！")

        except Exception as e:
            st.error(f"图片上传或数据写入失败：{e}")