import streamlit as st

def render_list(filtered_df):
    # Render rental listings as cards

    st.subheader(f"Listings ({len(filtered_df)})")

    if filtered_df.empty:
        st.warning("No listings match the selected filters")
        return

    for _, row in filtered_df.iterrows():
        with st.container(border=True):
            st.markdown(f"### {row['标题']}")
            st.markdown(f"**Suburb:** {row['区域']}")
            st.markdown(f"**Price:** ${row['价格']}/week")
            st.markdown(f"**Room Type:** {row['房型']}")
            st.markdown(f"**Bills Included:** {row['是否包bill']} | **Furnished:** {row['是否带家具']}")
            st.markdown(f"**Description:** {row['描述']}")
            st.markdown(f"**Phone:** {row['电话']}")
            st.markdown(f"**WeChat:** {row['微信']}")