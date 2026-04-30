import streamlit as st
import database
import folium
from streamlit_folium import st_folium
from image_service import upload_image_to_cloudinary

st.set_page_config(page_title="后台数据", layout="wide")

password = st.text_input("管理员密码", type="password")

if password != st.secrets.get("ADMIN_PASSWORD"):
    st.warning("请输入管理员密码")
    st.stop()

st.title("后台数据")

st.subheader("访问记录")
st.dataframe(database.get_table_dataframe("page_visits"))

st.subheader("房源点击")
st.dataframe(database.get_table_dataframe("listing_clicks"))

st.subheader("反馈")
st.dataframe(database.get_table_dataframe("feedback"))

st.subheader("房源")
df = database.get_all_listings()
st.dataframe(df)

if df.empty:
    st.info("暂无房源")
else:
    for _, row in df.iterrows():
        with st.expander(f"{row['标题']} - 当前状态：{row.get('status', 'active')}"):

            title = st.text_input("标题", value=row.get("标题", ""), key=f"title_{row['id']}")
            suburb = st.text_input("区域", value=row.get("区域", ""), key=f"suburb_{row['id']}")
            price = st.number_input("价格", value=int(row.get("价格", 0)), min_value=0, key=f"price_{row['id']}")
            room_type = st.selectbox(
                "房型",
                ["单间", "合租", "Studio", "整租"],
                index=["单间", "合租", "Studio", "整租"].index(row.get("房型", "单间"))
                if row.get("房型", "单间") in ["单间", "合租", "Studio", "整租"] else 0,
                key=f"room_{row['id']}"
            )

            latitude = float(row.get("纬度", -34.9285))
            longitude = float(row.get("经度", 138.6007))

            st.markdown("**当前位置**")
            m = folium.Map(location=[latitude, longitude], zoom_start=14)
            m.add_child(folium.LatLngPopup())
            folium.Marker([latitude, longitude]).add_to(m)

            map_data = st_folium(
                m,
                height=350,
                use_container_width=True,
                key=f"edit_map_{row['id']}"
            )

            if map_data and map_data.get("last_clicked"):
                latitude = map_data["last_clicked"]["lat"]
                longitude = map_data["last_clicked"]["lng"]

            st.write(f"当前纬度：{latitude}")
            st.write(f"当前经度：{longitude}")

            description = st.text_area("描述", value=row.get("描述", ""), key=f"desc_{row['id']}")

            old_image = row.get("图片", "")
            st.text_area("当前图片URL", value=old_image, key=f"old_img_{row['id']}")

            uploaded_file = st.file_uploader(
                "上传新图片（不上传则保留原图片）",
                type=["jpg", "png", "jpeg"],
                key=f"upload_{row['id']}"
            )

            contact = st.text_input("联系人", value=row.get("联系人", ""), key=f"contact_{row['id']}")
            phone = st.text_input("电话", value=row.get("电话", ""), key=f"phone_{row['id']}")
            wechat = st.text_input("微信", value=row.get("微信", ""), key=f"wechat_{row['id']}")

            bill = st.selectbox(
                "是否包 bill",
                ["是", "否"],
                index=0 if row.get("是否包bill", "否") == "是" else 1,
                key=f"bill_{row['id']}"
            )

            furniture = st.selectbox(
                "是否带家具",
                ["是", "否"],
                index=0 if row.get("是否带家具", "否") == "是" else 1,
                key=f"furniture_{row['id']}"
            )

            status = st.selectbox(
                "状态",
                ["active", "rented"],
                index=0 if row.get("status", "active") == "active" else 1,
                key=f"status_{row['id']}"
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button("保存修改", key=f"save_{row['id']}"):
                    new_image_url = upload_image_to_cloudinary(uploaded_file) if uploaded_file else old_image

                    database.update_listing(row["id"], {
                        "标题": title,
                        "区域": suburb,
                        "价格": int(price),
                        "房型": room_type,                       
                        "纬度": float(latitude),
                        "经度": float(longitude),
                        "描述": description,
                        "图片": new_image_url,
                        "联系人": contact,
                        "电话": phone,
                        "微信": wechat,
                        "是否包bill": bill,
                        "是否带家具": furniture,
                        "status": status
                    })
                    st.success("修改成功")
                    st.rerun()

            with col2:
                if status == "active":
                    if st.button("标记已出租", key=f"rent_{row['id']}"):
                        database.update_listing_status(row["id"], "rented")
                        st.success("已标记为已出租")
                        st.rerun()
                else:
                    if st.button("重新上架", key=f"active_{row['id']}"):
                        database.update_listing_status(row["id"], "active")
                        st.success("已重新上架")
                        st.rerun()