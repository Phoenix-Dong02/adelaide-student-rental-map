import streamlit as st
import folium
from streamlit_folium import st_folium

def render_map(filtered_df):

    st.subheader("地图看房")

    m = folium.Map(location=[-34.9285, 138.6007], zoom_start=12)

    for _, row in filtered_df.iterrows():
        images = row["图片"]
        if isinstance(images, str):
            images = [images]

        popup_html = f"""
        <div style='width:260px'>
            <h4>{row['标题']}</h4>
            <p><b>区域：</b>{row['区域']}</p>
            <p><b>价格：</b>${row['价格']}/week</p>
            <p><b>房型：</b>{row['房型']}</p>
            <p><b>联系人：</b>{row['联系人']}</p>
            <p><b>电话：</b>{row['电话']}</p>
            <p><b>微信：</b>{row['微信']}</p>
            <img src='{images[0]}' width='240' />
        </div>
        """

        folium.Marker(
            location=[row['纬度'], row['经度']],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{row['标题']} - ${row['价格']}/week"
        ).add_to(m)

    st_folium(m, height=700)