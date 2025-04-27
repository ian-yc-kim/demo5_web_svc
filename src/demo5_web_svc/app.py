import streamlit as st
import logging

# Set Streamlit page configuration
st.set_page_config(page_title="demo5_web_svc App", layout="wide")

# Sidebar navigation for switching between pages
page = st.sidebar.radio("Navigation", ("Signup", "Login", "Forum", "Meetings"))

try:
    if page == "Signup":
        from demo5_web_svc.pages.signup import render_signup_page
        render_signup_page()
    elif page == "Login":
        from demo5_web_svc.pages.login import login
        login()
    elif page == "Forum":
        from demo5_web_svc.pages.forum import render_forum_page
        render_forum_page()
    elif page == "Meetings":
        from demo5_web_svc.pages.meeting_appointment import render_meeting_appointment_page
        render_meeting_appointment_page()
except Exception as e:
    logging.error(e, exc_info=True)
    st.error("An error occurred while loading the page. Please try again later.")
