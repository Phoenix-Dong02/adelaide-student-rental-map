import streamlit as st
import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name=st.secrets["CLOUDINARY_CLOUD_NAME"],
    api_key=st.secrets["CLOUDINARY_API_KEY"],
    api_secret=st.secrets["CLOUDINARY_API_SECRET"],
    secure=True
)


def upload_image_to_cloudinary(uploaded_file):
    """
    Upload an image file to Cloudinary and return the hosted image URL.
    Returns an empty string if no file is provided.
    """
    if uploaded_file is None:
        return ""

    result = cloudinary.uploader.upload(
        uploaded_file,
        folder="adelaide-rental-map"
    )

    return result.get("secure_url", "")