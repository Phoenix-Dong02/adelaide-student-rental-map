import streamlit as st
import database

def render_list(filtered_df):
    # Render rental listings as cards

    st.subheader(f"房源列表（{len(filtered_df)}）")

    if filtered_df.empty:
        st.warning("没有符合当前筛选条件的房源")
        return

    for _, row in filtered_df.iterrows():
        with st.container(border=True):

            image_value = str(row["图片"]) if row["图片"] else ""
            image_url = image_value.split(",")[0].strip() if image_value else ""

            if image_url:
                st.image(image_url, use_container_width=True)

            st.markdown(f"### {row['标题']}")
            st.markdown(f"**区域：** {row['区域']}")
            st.markdown(f"**价格：** ${row['价格']}/周")
            st.markdown(f"**房型：** {row['房型']}")
            st.markdown(f"**是否包 bill：** {row['是否包bill']} ｜ **是否带家具：** {row['是否带家具']}")
            st.markdown(f"**描述：** {row['描述']}")
            st.markdown(f"**电话：** {row['电话']}")
            st.markdown(f"**微信：** {row['微信']}")
            st.caption("位置为大致范围，具体地址请联系房东。")

            if st.button("我感兴趣", key=row["id"]):
                database.record_listing_click(row["id"])
                st.success("已记录你的兴趣")