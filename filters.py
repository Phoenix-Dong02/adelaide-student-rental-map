import streamlit as st
def apply_filters(df):
    st.sidebar.header("筛选条件")

    room_type_options = ["全部"] + sorted(df["房型"].unique().tolist())
    selected_room_type = st.sidebar.selectbox("房型", room_type_options)

    min_price = int(df["价格"].min())
    max_price = int(df["价格"].max())
    selected_price = st.sidebar.slider("每周价格范围 ($/week)", min_price, max_price, (min_price, max_price))

    suburb_keyword = st.sidebar.text_input("搜索区域", "")

    bill_option = st.sidebar.selectbox("是否包bill", ["全部", "是", "否"])

    furniture_option = st.sidebar.selectbox("是否带家具", ["全部", "是", "否"])

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
    
    return filtered_df