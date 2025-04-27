import streamlit as st
import logging
from datetime import datetime
import requests
from email_validator import validate_email, EmailNotValidError


def create_meeting(payload: dict) -> tuple[bool, str]:
    """Create a meeting by calling the API endpoint.

    Args:
        payload (dict): Meeting data including time, location, and participants.

    Returns:
        tuple: A tuple where the first element is a boolean indicating success, and the second is a message.
    """
    try:
        headers = {"Content-Type": "application/json"}
        response = requests.post("http://localhost:8081/api/meetings", json=payload, headers=headers)
        if response.status_code in (200, 201):
            return True, "Meeting created successfully!"
        else:
            logging.error("API POST error: %s", response.text)
            return False, f"Failed to create meeting. Status: {response.status_code}"
    except Exception as e:
        logging.error(e, exc_info=True)
        return False, "An error occurred while creating the meeting."


def fetch_meetings() -> tuple[bool, any]:
    """Fetch the list of meetings from the API.

    Returns:
        tuple: A tuple where the first element is a boolean indicating success, and the second is either the meetings list or an error message.
    """
    try:
        response = requests.get("http://localhost:8081/api/meetings")
        if response.status_code == 200:
            meetings = response.json()
            return True, meetings
        else:
            logging.error("API GET error: %s", response.text)
            return False, f"Failed to fetch meetings. Status: {response.status_code}"
    except Exception as e:
        logging.error(e, exc_info=True)
        return False, "An error occurred while fetching the meetings."


def render_meeting_appointment_page() -> None:
    """Render the Meeting Appointment Page with creation form and meetings listing."""
    st.header("Meeting Appointment Page")

    # Meeting creation form
    with st.form("meeting_form", clear_on_submit=True):
        meeting_date = st.date_input("Meeting Date")
        meeting_time = st.time_input("Meeting Time")
        location = st.text_input("Location")
        participants_input = st.text_input("Participants (comma separated emails)")
        submitted = st.form_submit_button("Create Meeting")

        if submitted:
            try:
                meeting_datetime = datetime.combine(meeting_date, meeting_time)
                now = datetime.now()
                if meeting_datetime <= now:
                    st.error("Meeting time must be in the future.")
                elif not location.strip():
                    st.error("Location cannot be empty.")
                else:
                    participants = [email.strip() for email in participants_input.split(",") if email.strip()]
                    # Validate participant emails if provided
                    for email in participants:
                        try:
                            validate_email(email)
                        except EmailNotValidError:
                            st.error(f"Invalid email: {email}")
                            return
                    payload = {
                        "time": meeting_datetime.isoformat(),
                        "location": location.strip(),
                        "participants": participants
                    }
                    success, message = create_meeting(payload)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
            except Exception as e:
                logging.error(e, exc_info=True)
                st.error("An error occurred while processing the form.")

    # Meeting listing section
    st.subheader("Meetings List")

    # A refresh button - when clicked, the page will rerun
    if st.button("Refresh Meetings"):
        pass  # The page refreshes naturally on button click

    success, meetings_or_error = fetch_meetings()
    if success:
        meetings = meetings_or_error
        if meetings:
            st.table(meetings)
        else:
            st.info("No meetings scheduled.")
    else:
        st.error(meetings_or_error)
