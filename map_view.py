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

    m = folium.Map(location=[-34.9285, 138.6007], zoom_start=12)

    for _, row in filtered_df.iterrows():
        image_value = str(row["图片"]) if row["图片"] else ""
        first_image = image_value.split(",")[0].strip() if image_value else ""
        img_src = image_to_html_src(first_image)

        image_html = (
            f"<img src='{img_src}' width='100%' style='border-radius:8px'/>"
            if img_src else
            "<p><i>暂无图片</i></p>"
        )

        popup_html = f"""
        <div style='width:260px'>
            <h4>{row['标题']}</h4>
            <p><b>区域：</b> {row['区域']}</p>
            <p><b>价格：</b> ${row['价格']}/周</p>
            <p><b>房型：</b> {row['房型']}</p>
            <p><b>联系人：</b> {row['联系人']}</p>
            <p><b>电话：</b> {row['电话']}</p>
            <p><b>微信：</b> {row['微信']}</p>
            <p style='color:gray;font-size:12px'>
            位置为大致范围，具体地址请联系房东。
            </p>
            {image_html}
        </div>
        """

        status = row.get("status", "active")

        color = "red" if status == "active" else "gray"

        folium.Marker(
            location=[row["纬度"], row["经度"]],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{row['标题']} - ${row['价格']}/周",
            icon=folium.Icon(color=color)
        ).add_to(m)

    st_folium(m, height=900, use_container_width=True)