import streamlit as st
import database

st.set_page_config(page_title="Dashboard", layout="wide")

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
