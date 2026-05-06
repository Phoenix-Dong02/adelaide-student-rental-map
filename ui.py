import streamlit as st
import pandas as pd
import database


def move_selected_to_top(df):
    selected_id = st.session_state.get("selected_listing_id")

    if selected_id is None or df.empty:
        return df

    selected_df = df[df["id"] == selected_id]
    other_df = df[df["id"] != selected_id]

    if selected_df.empty:
        return df

    return pd.concat([selected_df, other_df], ignore_index=True)


def render_list(filtered_df, t):
    st.subheader(f"{t['listing_title']}{len(filtered_df)}）")

    if filtered_df.empty:
        st.warning(t["listing_empty"])
        return

    sorted_df = move_selected_to_top(filtered_df)

    visible_count = st.selectbox(
        t["listing_display_count"],
        [5, 10, 20, t["filter_all"]],
        index=0
    )

    if visible_count != t["filter_all"]:
        display_df = sorted_df.head(int(visible_count))
    else:
        display_df = sorted_df

    for _, row in display_df.iterrows():
        is_selected = row["id"] == st.session_state.get("selected_listing_id")

        with st.container(border=True):
            if is_selected:
                st.success(t["listing_selected"])

            image_value = str(row["图片"]) if row["图片"] else ""
            image_url = image_value.split(",")[0].strip() if image_value else ""

            if image_url:
                st.image(image_url, use_container_width=True)

            st.markdown(f"### {row['标题']}")
            st.markdown(f"<b>{t['listing_price']}</b> ${row['价格']}{t['filter_per_week']}", unsafe_allow_html=True)
            st.markdown(f"<b>{t['listing_room_type']}</b> {row['房型']}", unsafe_allow_html=True)
            st.markdown(f"<b>{t['listing_suburb']}</b> {row['区域']}", unsafe_allow_html=True)

            with st.expander(t["listing_details"]):
                st.markdown(f"<b>{t['listing_description']}</b> {row.get('描述', t['listing_no_data'])}", unsafe_allow_html=True)
                st.markdown(f"<b>{t['listing_contact']}</b> {row.get('联系人', t['listing_no_data'])}", unsafe_allow_html=True)
                st.markdown(f"<b>{t['listing_phone']}</b> {row.get('电话', t['listing_no_data'])}", unsafe_allow_html=True)
                st.markdown(f"<b>{t['listing_wechat']}</b> {row.get('微信', t['listing_no_data'])}", unsafe_allow_html=True)

            if st.button(t["listing_view_map"], key=f"view_{row['id']}"):
                st.session_state.selected_listing_id = row["id"]
                st.rerun()

            if st.button(t["listing_interested"], key=f"interest_{row['id']}"):
                database.record_listing_click(row["id"])
                st.success(t["listing_interest_recorded"])

def render_selected_listing(filtered_df, t):
    st.subheader(t["panel_title"])

    selected_id = st.session_state.get("selected_listing_id")

    if selected_id is None:
        st.info(t["panel_no_selection"])
        return

    selected_df = filtered_df[filtered_df["id"] == selected_id]

    if selected_df.empty:
        st.warning(t["panel_not_in_filter"])
        return

    row = selected_df.iloc[0]

    image_value = str(row["图片"]) if row["图片"] else ""
    image_url = image_value.split(",")[0].strip() if image_value else ""

    if image_url:
        st.image(image_url, use_container_width=True)

    st.markdown(f"### {row['标题']}")
    st.markdown(f"<b>{t['listing_price']}</b> ${row['价格']}{t['filter_per_week']}", unsafe_allow_html=True)
    st.markdown(f"<b>{t['listing_suburb']}</b> {row['区域']}", unsafe_allow_html=True)
    st.markdown(f"<b>{t['listing_room_type']}</b> {row['房型']}", unsafe_allow_html=True)
    st.markdown(f"<b>{t['listing_bill']}</b> {row['是否包bill']}", unsafe_allow_html=True)
    st.markdown(f"<b>{t['listing_furniture']}</b> {row['是否带家具']}", unsafe_allow_html=True)
    st.markdown(f"<b>{t['listing_description']}</b> {row.get('描述', t['listing_no_data'])}", unsafe_allow_html=True)
    st.markdown(f"<b>{t['listing_contact']}</b> {row.get('联系人', t['listing_no_data'])}", unsafe_allow_html=True)
    st.markdown(f"<b>{t['listing_phone']}</b> {row.get('电话', t['listing_no_data'])}", unsafe_allow_html=True)
    st.markdown(f"<b>{t['listing_wechat']}</b> {row.get('微信', t['listing_no_data'])}", unsafe_allow_html=True)

    if st.button(t["listing_interested"], key=f"interest_{row['id']}"):
        database.record_listing_click(row["id"])
        st.success(t["listing_interest_recorded"])