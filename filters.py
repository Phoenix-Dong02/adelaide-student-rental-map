import streamlit as st
import pandas as pd

def apply_filters(df, t):
    # Sidebar filter panel
    st.sidebar.header(t["filter_header"])

    # Handle empty dataset safely
    if df.empty:
        st.sidebar.info(t["filter_no_listings"])
        return df

    if "价格" not in df.columns or df["价格"].dropna().empty:
        st.sidebar.info(t["filter_no_price_data"])
        return df

    room_type_options = [t["filter_all"]] + sorted(df["房型"].dropna().unique().tolist())
    selected_room_type = st.sidebar.selectbox(t["filter_room_type"], room_type_options)

    min_price = int(df["价格"].min())
    max_price = int(df["价格"].max())

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

    bill_option = st.sidebar.selectbox(t["filter_bill"], [t["filter_all"], t["filter_yes"], t["filter_no"]])
    furniture_option = st.sidebar.selectbox(t["filter_furniture"], [t["filter_all"], t["filter_yes"], t["filter_no"]])

    filtered_df = df.copy()

    # Apply filters
    if selected_room_type != t["filter_all"]:
        filtered_df = filtered_df[filtered_df["房型"] == selected_room_type]

    filtered_df = filtered_df[
        (filtered_df["价格"] >= selected_price[0]) &
        (filtered_df["价格"] <= selected_price[1])
    ]

    if suburb_keyword.strip():
        filtered_df = filtered_df[
            filtered_df["区域"].str.contains(suburb_keyword, case=False, na=False)
        ]

    if bill_option != t["filter_all"]:
        filtered_df = filtered_df[
            filtered_df["是否包bill"] == bill_option
        ]

    if furniture_option != t["filter_all"]:
        filtered_df = filtered_df[
            filtered_df["是否带家具"] == furniture_option
        ]

    return filtered_df