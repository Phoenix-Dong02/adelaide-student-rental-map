import streamlit as st
import folium
from streamlit_folium import st_folium
import base64
import os


def image_to_html_src(image_path: str) -> str:
    # 空值直接返回空
    if not image_path:
        return ""

    # 网络图片，直接返回
    if image_path.startswith("http://") or image_path.startswith("https://"):
        return image_path

    # 兼容你现在可能存的 ./images/xxx.jpg
    normalized_path = image_path.replace("\\", "/")
    if normalized_path.startswith("./"):
        normalized_path = normalized_path[2:]

    # 本地文件不存在，就返回空
    if not os.path.exists(normalized_path):
        return ""

    # 根据扩展名简单判断 mime type
    ext = os.path.splitext(normalized_path)[1].lower()
    if ext == ".png":
        mime_type = "image/png"
    elif ext in [".jpg", ".jpeg"]:
        mime_type = "image/jpeg"
    else:
        mime_type = "application/octet-stream"

    # 读本地文件并转成 base64
    with open(normalized_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")

    return f"data:{mime_type};base64,{encoded}"


def render_map(filtered_df):
    st.subheader("地图看房")

    m = folium.Map(location=[-34.9285, 138.6007], zoom_start=12)

    for _, row in filtered_df.iterrows():
        image_value = row["图片"]

        if isinstance(image_value, str):
            images = [image_value]
        else:
            images = []

        img_src = image_to_html_src(images[0]) if images else ""

        if img_src:
            image_html = f"<img src='{img_src}' width='240' />"
        else:
            image_html = "<p>暂无图片</p>"

        popup_html = f"""
        <div style='width:260px'>
            <h4>{row['标题']}</h4>
            <p><b>区域：</b>{row['区域']}</p>
            <p><b>价格：</b>${row['价格']}/week</p>
            <p><b>房型：</b>{row['房型']}</p>
            <p><b>联系人：</b>{row['联系人']}</p>
            <p><b>电话：</b>{row['电话']}</p>
            <p><b>微信：</b>{row['微信']}</p>
            {image_html}
        </div>
        """

        folium.Marker(
            location=[row['纬度'], row['经度']],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{row['标题']} - ${row['价格']}/week"
        ).add_to(m)

    st_folium(m, height=700)