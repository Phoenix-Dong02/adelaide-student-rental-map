import streamlit as st
import pandas as pd

def apply_filters(df):
    # Sidebar filter panel
    st.sidebar.header("筛选条件")

    # Handle empty dataset safely
    if df.empty:
        st.sidebar.info("暂无房源")
        return df

    if "价格" not in df.columns or df["价格"].dropna().empty:
        st.sidebar.info("暂无有效价格数据")
        return df

    room_type_options = ["全部"] + sorted(df["房型"].dropna().unique().tolist())
    selected_room_type = st.sidebar.selectbox("房型", room_type_options)

    min_price = int(df["价格"].min())
    max_price = int(df["价格"].max())

    if min_price == max_price:
        st.sidebar.write(f"当前价格：${min_price}/周")
        selected_price = (min_price, max_price)
    else:
        selected_price = st.sidebar.slider(
            "每周租金范围（澳元/周）",
            min_price,
            max_price,
            (min_price, max_price)
        )

    suburb_keyword = st.sidebar.text_input("搜索区域", "")

    bill_option = st.sidebar.selectbox("是否包 bill", ["全部", "是", "否"])
    furniture_option = st.sidebar.selectbox("是否带家具", ["全部", "是", "否"])

    filtered_df = df.copy()

    # Apply filters
    if selected_room_type != "全部":
        filtered_df = filtered_df[filtered_df["房型"] == selected_room_type]

    filtered_df = filtered_df[
        (filtered_df["价格"] >= selected_price[0]) &
        (filtered_df["价格"] <= selected_price[1])
    ]

    if suburb_keyword.strip():
        filtered_df = filtered_df[
            filtered_df["区域"].str.contains(suburb_keyword, case=False, na=False)
        ]

    if bill_option != "全部":
        filtered_df = filtered_df[
            filtered_df["是否包bill"] == bill_option
        ]

    if furniture_option != "全部":
        filtered_df = filtered_df[
            filtered_df["是否带家具"] == furniture_option
        ]

    return filtered_df