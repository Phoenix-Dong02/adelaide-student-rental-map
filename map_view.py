import streamlit as st
import folium
from streamlit_folium import st_folium
import base64
import os

def image_to_html_src(image_path: str) -> str:
    # Convert image path (local or URL) into HTML display format

    if not image_path:
        return ""

    if image_path.startswith("http://") or image_path.startswith("https://"):
        return image_path

    normalized_path = image_path.replace("\\", "/")

    if not os.path.exists(normalized_path):
        return ""

    with open(normalized_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")

    return f"data:image/jpeg;base64,{encoded}"


def render_map(filtered_df):
    # Render interactive map with listing markers

    st.subheader("Map View")

    m = folium.Map(location=[-34.9285, 138.6007], zoom_start=12)

    for _, row in filtered_df.iterrows():
        img_src = image_to_html_src(row["图片"])

        popup_html = f"""
        <div style='width:260px'>
            <h4>{row['标题']}</h4>
            <p><b>Suburb:</b> {row['区域']}</p>
            <p><b>Price:</b> ${row['价格']}/week</p>
            <p><b>Room Type:</b> {row['房型']}</p>
            <p><b>Contact:</b> {row['联系人']}</p>
            <p><b>Phone:</b> {row['电话']}</p>
            <p><b>WeChat:</b> {row['微信']}</p>
            <img src='{img_src}' width='240'/>
        </div>
        """

        folium.Marker(
            location=[row['纬度'], row['经度']],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{row['标题']} - ${row['价格']}/week"
        ).add_to(m)

    st_folium(m, height=700)