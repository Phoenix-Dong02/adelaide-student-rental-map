import streamlit as st

def render_list(filtered_df):
    st.title("阿德莱德留学生租房地图")
    st.caption("面向中文用户的租房筛选平台：地图看房源，点击查看联系人和房屋信息")

    st.subheader(f"房源列表（{len(filtered_df)}）")

    if filtered_df.empty:
        st.warning("没有符合条件的房源")
        return

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