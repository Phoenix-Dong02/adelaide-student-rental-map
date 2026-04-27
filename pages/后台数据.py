import streamlit as st
import database

st.set_page_config(page_title="后台数据", layout="wide")

password = st.text_input("管理员密码", type="password")

if password != st.secrets.get("ADMIN_PASSWORD"):
    st.warning("请输入管理员密码")
    st.stop()

st.title("后台数据")

st.subheader("访问记录")
st.dataframe(database.get_table_dataframe("page_visits"))

st.subheader("房源点击")
st.dataframe(database.get_table_dataframe("listing_clicks"))

st.subheader("反馈")
st.dataframe(database.get_table_dataframe("feedback"))

st.subheader("房源")
df = database.get_all_listings()
st.dataframe(df)

if df.empty:
    st.info("暂无房源")
else:
    for _, row in df.iterrows():
        st.write(f"{row['标题']} - 当前状态：{row.get('status', 'active')}")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("标记已出租", key=f"rent_{row['id']}"):
                database.update_listing_status(row["id"], "rented")
                st.success("已标记为已出租")
                st.rerun()

        with col2:
            if st.button("重新上架", key=f"active_{row['id']}"):
                database.update_listing_status(row["id"], "active")
                st.success("已重新上架")
                st.rerun()