import streamlit as st
import pandas as pd
from translations import translate_value

def apply_filters(df, t):
    # Sidebar filter panel
    st.sidebar.header(t["filter_header"])

    df["价格"] = pd.to_numeric(df["价格"], errors="coerce")

    # Handle empty dataset safely
    if df.empty:
        st.sidebar.info(t["filter_no_listings"])
        return df

    if "价格" not in df.columns or df["价格"].dropna().empty:
        st.sidebar.info(t["filter_no_price_data"])
        return df

    lang = st.session_state.get("lang", "zh")

    # 选项值用中文规范值，None 表示"全部"；format_func 只负责显示
    def format_option(value):
        return t["filter_all"] if value is None else translate_value(value, lang)

    room_type_options = [None] + sorted(df["房型"].dropna().unique().tolist())
    selected_room_type = st.sidebar.selectbox(t["filter_room_type"], room_type_options, format_func=format_option)

    price_series = pd.to_numeric(df["价格"], errors="coerce").dropna()
    min_price = int(price_series.min())
    max_price = int(price_series.max())

    if min_price == max_price:
        st.sidebar.write(f"{t['filter_current_price']}${min_price}{t['filter_per_week']}")
        selected_price = (min_price, max_price)
    else:
        selected_price = st.sidebar.slider(
            t["filter_price_range"],
            min_price,
            max_price,
            (min_price, max_price)
        )

    suburb_keyword = st.sidebar.text_input(t["filter_suburb"], "")

    bill_option = st.sidebar.selectbox(t["filter_bill"], [None, "是", "否"], format_func=format_option)
    furniture_option = st.sidebar.selectbox(t["filter_furniture"], [None, "是", "否"], format_func=format_option)

    filtered_df = df.copy()

    # Apply filters
    if selected_room_type is not None:
        filtered_df = filtered_df[filtered_df["房型"] == selected_room_type]

    filtered_df = filtered_df[
        (filtered_df["价格"] >= selected_price[0]) &
        (filtered_df["价格"] <= selected_price[1])
    ]

    if suburb_keyword.strip():
        filtered_df = filtered_df[
            filtered_df["区域"].str.contains(suburb_keyword, case=False, na=False)
        ]

    if bill_option is not None:
        filtered_df = filtered_df[
            filtered_df["是否包bill"] == bill_option
        ]

    if furniture_option is not None:
        filtered_df = filtered_df[
            filtered_df["是否带家具"] == furniture_option
        ]

    return filtered_df