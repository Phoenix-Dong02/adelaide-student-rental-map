import folium
from streamlit_folium import st_folium
import math

from translate_service import translate_text


def image_to_html_src(image_path: str) -> str:
    if image_path and (image_path.startswith("http://") or image_path.startswith("https://")):
        return image_path
    return ""


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


def render_map(filtered_df, t):
    center_lat = -34.9285
    center_lng = 138.6007
    zoom = 12


    m = folium.Map(location=[center_lat, center_lng], zoom_start=zoom)
    lang = t.get("lang_code", "zh")

    for _, row in filtered_df.iterrows():
        image_value = str(row["图片"]) if row["图片"] else ""
        first_image = image_value.split(",")[0].strip() if image_value else ""
        img_src = image_to_html_src(first_image)
        title = translate_text(row["标题"], lang)

        image_html = (
            f"<img src='{img_src}' width='100%' style='border-radius:8px'/>"
            if img_src else
            f"<p><i>{t['map_no_image']}</i></p>"
        )

        popup_html = f"""
            <div style='width:240px'>
                {image_html}
                <h4>{title}</h4>
                <p><b>${row['价格']}{t['filter_per_week']}</b></p>
                <p style='color:gray;font-size:12px'>
                    {t['map_view_info']}
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
            tooltip=f"{title} - ${row['价格']}{t['filter_per_week']}",
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

    