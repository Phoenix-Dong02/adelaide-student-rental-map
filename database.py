import streamlit as st
import pandas as pd
from supabase import create_client


@st.cache_resource
def get_supabase_client():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)


# Keep these functions so old code will not break.
# Tables are now created in Supabase SQL Editor, not inside Python.
def create_table():
    pass


def migrate_database():
    pass


def create_tracking_tables():
    pass


def insert_listing(listing):
    supabase = get_supabase_client()
    return supabase.table("listings").insert(listing).execute()


def get_active_listings():
    supabase = get_supabase_client()
    response = (
        supabase
        .table("listings")
        .select("*")
        .eq("status", "active")
        .order("id", desc=True)
        .execute()
    )
    return pd.DataFrame(response.data)


def get_all_listings():
    supabase = get_supabase_client()
    response = (
        supabase
        .table("listings")
        .select("*")
        .order("id", desc=True)
        .execute()
    )
    return pd.DataFrame(response.data)


def count_listings():
    supabase = get_supabase_client()
    response = supabase.table("listings").select("id").execute()
    return len(response.data)


def record_page_visit():
    supabase = get_supabase_client()
    return supabase.table("page_visits").insert({}).execute()


def record_listing_click(listing_id):
    supabase = get_supabase_client()
    return supabase.table("listing_clicks").insert({
        "listing_id": int(listing_id)
    }).execute()


def insert_feedback(content):
    supabase = get_supabase_client()
    return supabase.table("feedback").insert({
        "content": content
    }).execute()


def get_table_dataframe(table_name):
    supabase = get_supabase_client()
    response = (
        supabase
        .table(table_name)
        .select("*")
        .order("id", desc=True)
        .execute()
    )
    return pd.DataFrame(response.data)


def update_listing_status(listing_id, status):
    supabase = get_supabase_client()
    return (
        supabase
        .table("listings")
        .update({"status": status})
        .eq("id", int(listing_id))
        .execute()
    )

def update_listing(listing_id, updated_data):
    supabase = get_supabase_client()
    return (
        supabase
        .table("listings")
        .update(updated_data)
        .eq("id", int(listing_id))
        .execute()
    ) 