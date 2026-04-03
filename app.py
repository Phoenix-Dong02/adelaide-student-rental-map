import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="阿德莱德留学生租房地图", layout="wide")

# -----------------------------
# 1. Mock rental data
# -----------------------------
listings = [
    {
        "id": 1,
        "标题": "阿德莱德CBD 近大学女生双人间床位",
        "区域": "Adelaide CBD",
        "价格": 230,
        "房型": "合租",
        "纬度": -34.9285,
        "经度": 138.6007,
        "描述": "步行可到阿大，近Rundle Mall，适合预算有限学生。",
        "图片": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=80",
        "联系人": "Amy",
        "电话": "0412 345 678",
        "微信": "amy-rent-cbd",
        "是否包bill": "是",
        "是否带家具": "是"
    },
    {
        "id": 2,
        "标题": "North Adelaide 独立Studio",
        "区域": "North Adelaide",
        "价格": 315,
        "房型": "Studio",
        "纬度": -34.9071,
        "经度": 138.5947,
        "描述": "安静安全，适合喜欢独立空间的学生。",
        "图片": "https://images.unsplash.com/photo-1484154218962-a197022b5858?auto=format&fit=crop&w=1200&q=80",
        "联系人": "Leo",
        "电话": "0433 222 111",
        "微信": "leo-studio-na",
        "是否包bill": "否",
        "是否带家具": "是"
    },
    {
        "id": 3,
        "标题": "Norwood 单间招租",
        "区域": "Norwood",
        "价格": 250,
        "房型": "单间",
        "纬度": -34.9212,
        "经度": 138.6346,
        "描述": "周边中餐多，生活方便，公交进城快。",
        "图片": "https://images.unsplash.com/photo-1494526585095-c41746248156?auto=format&fit=crop&w=1200&q=80",
        "联系人": "Daniel",
        "电话": "0422 666 444",
        "微信": "daniel-norwood-room",
        "是否包bill": "是",
        "是否带家具": "否"
    },
    {
        "id": 4,
        "标题": "Prospect 两室一厅整租",
        "区域": "Prospect",
        "价格": 320,
        "房型": "整租",
        "纬度": -34.8840,
        "经度": 138.5940,
        "描述": "适合情侣或朋友一起合租，生活氛围好。",
        "图片": "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=1200&q=80",
        "联系人": "Grace",
        "电话": "0411 888 555",
        "微信": "grace-prospect-home",
        "是否包bill": "否",
        "是否带家具": "是"
    },
    {
        "id": 5,
        "标题": "Mawson Lakes 便宜合租房",
        "区域": "Mawson Lakes",
        "价格": 185,
        "房型": "合租",
        "纬度": -34.8153,
        "经度": 138.6103,
        "描述": "价格低，适合预算敏感型学生。",
        "图片": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=80",
        "联系人": "Kevin",
        "电话": "0400 111 222",
        "微信": "kevin-mawson-share",
        "是否包bill": "是",
        "是否带家具": "是"
    },
    {"id": 6,
        "标题": "burnside 便宜合租房",
        "区域": "burnside",
        "价格": 170,
        "房型": "合租",
        "纬度": -34.9497,
        "经度": 138.6530,
        "描述": "价格低，适合预算敏感型学生。",
        "图片": [
    "images/IMG_3266.JPG",
    "images/IMG_3267.JPG",
    "images/IMG_3268.JPG"
],
        "联系人": "houbingtao",
        "电话": "0400 111 222",
        "微信": "houbingtao1974",
        "是否包bill": "否",
        "是否带家具": "是"}

]

df = pd.DataFrame(listings)

# -----------------------------
# 2. Page header
# -----------------------------
st.title("阿德莱德留学生租房地图")
st.caption("面向中文用户的租房筛选平台：地图看房源，点击查看联系人和房屋信息")

# -----------------------------
# 3. Sidebar filters
# -----------------------------
st.sidebar.header("筛选条件")

room_type_options = ["全部"] + sorted(df["房型"].unique().tolist())
selected_room_type = st.sidebar.selectbox("房型", room_type_options)

min_price = int(df["价格"].min())
max_price = int(df["价格"].max())
selected_price = st.sidebar.slider("每周价格范围 ($/week)", min_price, max_price, (min_price, max_price))

suburb_keyword = st.sidebar.text_input("搜索区域", "")

bill_option = st.sidebar.selectbox("是否包bill", ["全部", "是", "否"])

furniture_option = st.sidebar.selectbox("是否带家具", ["全部", "是", "否"])

# -----------------------------
# 4. Data filtering
# -----------------------------
filtered_df = df.copy()

if selected_room_type != "全部":
    filtered_df = filtered_df[filtered_df["房型"] == selected_room_type]

filtered_df = filtered_df[
    (filtered_df["价格"] >= selected_price[0]) &
    (filtered_df["价格"] <= selected_price[1])
]

if suburb_keyword.strip():
    filtered_df = filtered_df[filtered_df["区域"].str.contains(suburb_keyword, case=False, na=False)]

if bill_option != "全部":
    filtered_df = filtered_df[filtered_df["是否包bill"] == bill_option]

if furniture_option != "全部":
    filtered_df = filtered_df[filtered_df["是否带家具"] == furniture_option]

# -----------------------------
# 5. Main layout: listing panel + map panel
# -----------------------------
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader(f"房源列表（{len(filtered_df)}）")

    if filtered_df.empty:
        st.warning("没有符合条件的房源")
    else:
        for _, row in filtered_df.iterrows():
            with st.container(border=True):
                st.markdown(f"### {row['标题']}")
                st.markdown(f"**区域：** {row['区域']}")
                st.markdown(f"**价格：** ${row['价格']}/week")
                st.markdown(f"**房型：** {row['房型']}")
                st.markdown(f"**包bill：** {row['是否包bill']} | **带家具：** {row['是否带家具']}")
                st.markdown(f"**描述：** {row['描述']}")
                st.markdown(f"**电话：** {row['电话']}")
                st.markdown(f"**微信：** {row['微信']}")
                images = row["图片"]
if isinstance(images, str):
    images = [images]

 # Initialize image index for each listing
key = f"img_index_{row['id']}"
if key not in st.session_state:
    st.session_state[key] = 0

# Left and right button
col_left, col_right = st.columns([1, 1])

with col_left:
    if st.button("⬅️", key=f"left_{row['id']}"):
        st.session_state[key] = max(0, st.session_state[key] - 1)

with col_right:
    if st.button("➡️", key=f"right_{row['id']}"):
        st.session_state[key] = min(len(images) - 1, st.session_state[key] + 1)

# Current image display
st.image(images[st.session_state[key]], use_container_width=True)
# -----------------------------
# 6. Map visualization
# -----------------------------
with col2:
    st.subheader("地图看房")

    m = folium.Map(location=[-34.9285, 138.6007], zoom_start=12)

    for _, row in filtered_df.iterrows():
        images = row["图片"]
        if isinstance(images, str):
            images = [images]
        popup_html = f"""
<div style='width:260px'>
    <h4>{row['标题']}</h4>
    <p><b>区域：</b>{row['区域']}</p>
    <p><b>价格：</b>${row['价格']}/week</p>
    <p><b>房型：</b>{row['房型']}</p>
    <p><b>联系人：</b>{row['联系人']}</p>
    <p><b>电话：</b>{row['电话']}</p>
    <p><b>微信：</b>{row['微信']}</p>
    <img src='{images[0]}' width='240' style='border-radius:8px; margin-top:8px;' />
</div>
"""

        folium.Marker(
            location=[row['纬度'], row['经度']],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{row['标题']} - ${row['价格']}/week"
        ).add_to(m)

    st_folium(m, width=None, height=700)

# -----------------------------
# 7. Table display
# -----------------------------
st.subheader("筛选结果表")
st.dataframe(
    filtered_df[["标题", "区域", "价格", "房型", "是否包bill", "是否带家具", "联系人", "电话", "微信"]],
    use_container_width=True
)
