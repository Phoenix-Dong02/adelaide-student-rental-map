import streamlit as st
import pandas as pd
import database

st.set_page_config(page_title="后台数据", layout="wide")

password = st.text_input("管理员密码", type="password")

if password != st.secrets.get("ADMIN_PASSWORD"):
    st.warning("请输入管理员密码")
    st.stop()

st.title("后台数据")

conn = database.get_connection()

st.subheader("访问记录")
st.dataframe(pd.read_sql("SELECT * FROM page_visits ORDER BY id DESC", conn))

st.subheader("房源点击")
st.dataframe(pd.read_sql("SELECT * FROM listing_clicks ORDER BY id DESC", conn))

st.subheader("反馈")
st.dataframe(pd.read_sql("SELECT * FROM feedback ORDER BY id DESC", conn))

st.subheader("房源")
st.dataframe(pd.read_sql("SELECT * FROM listings ORDER BY id DESC", conn))
df = pd.read_sql("SELECT * FROM listings ORDER BY id DESC", conn)

for _, row in df.iterrows():
    st.write(f"{row['标题']} - 当前状态：{row.get('status','active')}")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("标记已出租", key=f"rent_{row['id']}"):
            conn.execute(
                "UPDATE listings SET status='rented' WHERE id=?",
                (row["id"],)
            )
            conn.commit()
            st.success("已标记为已出租")
            st.rerun()

    with col2:
        if st.button("重新上架", key=f"active_{row['id']}"):
            conn.execute(
                "UPDATE listings SET status='active' WHERE id=?",
                (row["id"],)
            )
            conn.commit()
            st.success("已重新上架")
            st.rerun()

conn.close()