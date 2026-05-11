from posthog import Posthog
import streamlit as st

posthog = Posthog(
    project_api_key=st.secrets["POSTHOG_API_KEY"],
    host=st.secrets["POSTHOG_HOST"]
)

def capture_event(event_name, properties=None):
    try:
        posthog.capture(
            distinct_id="anonymous_user",
            event=event_name,
            properties=properties or {}
        )
    except Exception:
        pass