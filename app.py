import streamlit as st
import pandas as pd
import os

import data
import filters
import map_view
import ui
import database

st.set_page_config(page_title="阿德莱德留学生租房地图", layout="wide")

database.create_table()

conn = database.get_connection()
count = pd.read_sql("SELECT COUNT(*) as count FROM listings", conn).iloc[0]["count"]

if count == 0:
    seed_df = data.get_seed_dataframe()
    seed_df.to_sql("listings", conn, if_exists="append", index=False)

conn.close()

st.subheader("发布房源")

with st.form("listing_form"):
    title = st.text_input("标题")
    suburb = st.text_input("区域")
    price = st.number_input("价格", min_value=0, step=1)
    room_type = st.selectbox("房型", ["合租", "单间", "Studio", "整租"])
    latitude = st.number_input("纬度", value=-34.9285, format="%.6f")
    longitude = st.number_input("经度", value=138.6007, format="%.6f")
    description = st.text_area("描述")
    uploaded_file = st.file_uploader("上传图片", type=["jpg", "png", "jpeg"])

    contact = st.text_input("联系人")
    phone = st.text_input("电话")
    wechat = st.text_input("微信")
    bill = st.selectbox("是否包bill", ["是", "否"])
    furniture = st.selectbox("是否带家具", ["是", "否"])

    submitted = st.form_submit_button("发布")

    if submitted:
        if uploaded_file is not None:
            os.makedirs("images", exist_ok=True)
            image_path = f"images/{uploaded_file.name}"

            with open(image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        else:
            image_path = ""

        database.insert_listing({
            "标题": title,
            "区域": suburb,
            "价格": int(price),
            "房型": room_type,
            "纬度": float(latitude),
            "经度": float(longitude),
            "描述": description,
            "图片": image_path,
            "联系人": contact,
            "电话": phone,
            "微信": wechat,
            "是否包bill": bill,
            "是否带家具": furniture
        })

        st.success("房源发布成功！")
        st.rerun()

df = data.get_dataframe()
filtered_df = filters.apply_filters(df)

col1, col2 = st.columns([1, 2])

with col1:
    ui.render_list(filtered_df)

with col2:
    map_view.render_map(filtered_df)