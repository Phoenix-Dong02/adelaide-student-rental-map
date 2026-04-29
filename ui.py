import streamlit as st
import database


def move_selected_to_top(df):
    selected_id = st.session_state.get("selected_listing_id")

    if selected_id is None or df.empty:
        return df

    selected_df = df[df["id"] == selected_id]
    other_df = df[df["id"] != selected_id]

    if selected_df.empty:
        return df

    return selected_df._append(other_df, ignore_index=True)


def render_list(filtered_df):
    st.subheader(f"房源列表（{len(filtered_df)}）")

    if filtered_df.empty:
        st.warning("没有符合当前筛选条件的房源")
        return

    sorted_df = move_selected_to_top(filtered_df)

    visible_count = st.selectbox(
        "显示数量",
        [5, 10, 20, "全部"],
        index=0
    )

    if visible_count != "全部":
        display_df = sorted_df.head(int(visible_count))
    else:
        display_df = sorted_df

    for _, row in display_df.iterrows():
        is_selected = row["id"] == st.session_state.get("selected_listing_id")

        with st.container(border=True):
            if is_selected:
                st.success("当前选中")

            image_value = str(row["图片"]) if row["图片"] else ""
            image_url = image_value.split(",")[0].strip() if image_value else ""

            if image_url:
                st.image(image_url, use_container_width=True)

            st.markdown(f"### {row['标题']}")
            st.markdown(f"**价格：** ${row['价格']}/周")
            st.markdown(f"**房型：** {row['房型']}")
            st.markdown(f"**区域：** {row['区域']}")

            with st.expander("查看详细信息"):
                st.markdown(f"**描述：** {row.get('描述', '暂无')}")
                st.markdown(f"**联系人：** {row.get('联系人', '暂无')}")
                st.markdown(f"**电话：** {row.get('电话', '暂无')}")
                st.markdown(f"**微信：** {row.get('微信', '暂无')}")

            if st.button("查看地图位置", key=f"view_{row['id']}"):
                st.session_state.selected_listing_id = row["id"]
                st.rerun()

            if st.button("我感兴趣", key=f"interest_{row['id']}"):
                database.record_listing_click(row["id"])
                st.success("已记录你的兴趣")

def render_selected_listing(filtered_df):
    st.subheader("房源详情")

    selected_id = st.session_state.get("selected_listing_id")

    if selected_id is None:
        st.info("点击地图上的房源点，查看详细信息")
        return

    selected_df = filtered_df[filtered_df["id"] == selected_id]

    if selected_df.empty:
        st.warning("当前房源不在筛选结果中")
        return

    row = selected_df.iloc[0]

    image_value = str(row["图片"]) if row["图片"] else ""
    image_url = image_value.split(",")[0].strip() if image_value else ""

    if image_url:
        st.image(image_url, use_container_width=True)

    st.markdown(f"### {row['标题']}")
    st.markdown(f"**价格：** ${row['价格']}/周")
    st.markdown(f"**区域：** {row['区域']}")
    st.markdown(f"**房型：** {row['房型']}")
    st.markdown(f"**是否包 bill：** {row['是否包bill']}")
    st.markdown(f"**是否带家具：** {row['是否带家具']}")
    st.markdown(f"**描述：** {row.get('描述', '暂无')}")
    st.markdown(f"**联系人：** {row.get('联系人', '暂无')}")
    st.markdown(f"**电话：** {row.get('电话', '暂无')}")
    st.markdown(f"**微信：** {row.get('微信', '暂无')}")

    if st.button("我感兴趣", key=f"interest_{row['id']}"):
        database.record_listing_click(row["id"])
        st.success("已记录你的兴趣")