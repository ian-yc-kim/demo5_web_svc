import os
import logging

import streamlit as st
import requests
from email_validator import validate_email, EmailNotValidError

# Set page configuration
st.set_page_config(page_title="Signup", layout="centered")


def validate_inputs(email: str, password: str, oauth_token: str) -> (bool, str):
    """
    Validate the signup form inputs.

    :param email: User email address
    :param password: User password
    :param oauth_token: Google OAuth token/authorization code
    :return: Tuple of (is_valid, error_message)
    """
    try:
        # Validate email using email_validator with deliverability check disabled
        validate_email(email, check_deliverability=False)
    except EmailNotValidError as e:
        return False, f"Invalid email: {str(e)}"

    if len(password) < 8:
        return False, "Password must be at least 8 characters long."

    if not oauth_token.strip():
        return False, "Google OAuth token/authorization code is required."

    return True, ""


def perform_signup_request(email: str, password: str, oauth_token: str) -> (bool, str):
    """
    Calls the auth-service signup API endpoint with the provided credentials.

    :param email: User email
    :param password: User password
    :param oauth_token: Google OAuth token/authorization code
    :return: Tuple of (is_success, message_or_token)
    """
    auth_service_url = os.getenv("AUTH_SERVICE_URL", "http://localhost:5000")
    url = f"{auth_service_url}/api/signup"
    payload = {
        "email": email,
        "password": password,
        "google_oauth_token": oauth_token
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        if "jwt_token" in data:
            return True, data["jwt_token"]
        else:
            return False, "Signup failed: JWT token not received."
    except Exception as e:
        logging.error(e, exc_info=True)
        return False, f"Signup error: {str(e)}"


# Streamlit UI implementation for Signup Page

def render_signup_page() -> None:
    st.title("Signup")
    
    with st.form(key="signup_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        oauth_token = st.text_input("Google OAuth Token / Authorization Code")

        submit_button = st.form_submit_button(label="Sign Up")

    if submit_button:
        is_valid, message = validate_inputs(email, password, oauth_token)
        if not is_valid:
            st.error(message)
        else:
            success, result = perform_signup_request(email, password, oauth_token)
            if success:
                st.success("Signup successful!")
                # Store JWT token in session state
                st.session_state['jwt_token'] = result
            else:
                st.error(result)


if __name__ == "__main__":
    render_signup_page()
