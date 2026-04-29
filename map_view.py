import streamlit as st
import folium
from streamlit_folium import st_folium
import base64
import os
import math


def image_to_html_src(image_path: str) -> str:
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


def find_nearest_listing_id(filtered_df, lat, lng):
    if filtered_df.empty:
        return None

    nearest_id = None
    nearest_distance = float("inf")

    for _, row in filtered_df.iterrows():
        distance = math.sqrt(
            (float(row["纬度"]) - lat) ** 2 +
            (float(row["经度"]) - lng) ** 2
        )

        if distance < nearest_distance:
            nearest_distance = distance
            nearest_id = row["id"]

    return nearest_id


def render_map(filtered_df):
    selected_id = st.session_state.get("selected_listing_id")

    center_lat = -34.9285
    center_lng = 138.6007
    zoom = 12


    m = folium.Map(location=[center_lat, center_lng], zoom_start=zoom)

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
            <div style='width:240px'>
                {image_html}
                <h4>{row['标题']}</h4>
                <p><b>${row['价格']}/周</b></p>
                <p style='color:gray;font-size:12px'>
                    左侧查看完整信息
                </p>
            </div>
        """

        status = row.get("status", "active")
        color = "red" if status == "active" else "gray"

        popup = folium.Popup(
            popup_html,
            max_width=300
        )

        folium.Marker(
            location=[row["纬度"], row["经度"]],
            popup=popup,
            tooltip=f"{row['标题']} - ${row['价格']}/周",
            icon=folium.Icon(color=color)
        ).add_to(m)

    map_data = st_folium(
        m,
        height=900,
        use_container_width=True,
        key="rental_map"
        
    )
    if map_data and map_data.get("last_object_clicked"):
        clicked_lat = map_data["last_object_clicked"]["lat"]
        clicked_lng = map_data["last_object_clicked"]["lng"]

        nearest_id = find_nearest_listing_id(filtered_df, clicked_lat, clicked_lng)

        if nearest_id is not None:
            return nearest_id

    return None

    