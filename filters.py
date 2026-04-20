import streamlit as st

def apply_filters(df):
    # Sidebar filter panel

    st.sidebar.header("Filters")

    room_type_options = ["All"] + sorted(df["房型"].unique().tolist())
    selected_room_type = st.sidebar.selectbox("Room Type", room_type_options)

    min_price = int(df["价格"].min())
    max_price = int(df["价格"].max())
    selected_price = st.sidebar.slider(
        "Weekly Price Range ($/week)", min_price, max_price, (min_price, max_price)
    )

    suburb_keyword = st.sidebar.text_input("Search Suburb", "")

    bill_option = st.sidebar.selectbox("Bills Included", ["All", "Yes", "No"])
    furniture_option = st.sidebar.selectbox("Furnished", ["All", "Yes", "No"])

    filtered_df = df.copy()

    # Apply filters
    if selected_room_type != "All":
        filtered_df = filtered_df[filtered_df["房型"] == selected_room_type]

    filtered_df = filtered_df[
        (filtered_df["价格"] >= selected_price[0]) &
        (filtered_df["价格"] <= selected_price[1])
    ]

    if suburb_keyword.strip():
        filtered_df = filtered_df[
            filtered_df["区域"].str.contains(suburb_keyword, case=False, na=False)
        ]

    if bill_option != "All":
        filtered_df = filtered_df[
            filtered_df["是否包bill"] == ("是" if bill_option == "Yes" else "否")
        ]

    if furniture_option != "All":
        filtered_df = filtered_df[
            filtered_df["是否带家具"] == ("是" if furniture_option == "Yes" else "否")
        ]

    return filtered_df