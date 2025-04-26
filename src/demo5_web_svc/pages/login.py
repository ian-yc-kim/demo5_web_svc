import streamlit as st
import requests
import logging
from email_validator import validate_email, EmailNotValidError
from demo5_web_svc import config

"""
Login Page Module

This module implements the Login UI using Streamlit. It captures user credentials,
validates input using the email_validator library, and integrates with the auth-service
for authentication. The auth-service URL is configured in config.AUTH_SERVICE_URL to avoid hardcoding.
"""

# Configure the Streamlit page
st.set_page_config(page_title="Login Page", layout="centered")


def attempt_login(email: str, password: str, oauth_token: str) -> dict:
    """Attempt to login using the provided credentials by calling the auth-service.

    Args:
        email (str): User's email address
        password (str): User's password
        oauth_token (str): Optional Google OAuth token

    Returns:
        dict: A dictionary containing the result of the login attempt. On success, returns
              {'success': True, 'token': <JWT token>}. On failure, returns
              {'success': False, 'error': <error message>}.
    """
    # Build the auth-service URL from the configuration
    url = f"{config.AUTH_SERVICE_URL}/api/login"

    # Prepare payload; include oauth_token only if provided
    payload = {
        "email": email,
        "password": password
    }
    if oauth_token:
        payload["oauth_token"] = oauth_token

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        if response.status_code == 200:
            result = response.json()
            return {"success": True, "token": result.get("token")}
        else:
            result = response.json()
            return {"success": False, "error": result.get("error", "Unknown error")}
    except Exception as e:
        logging.error(e, exc_info=True)
        return {"success": False, "error": "Request failed"}


def login() -> None:
    """Render the login page UI and handle form submission for user login."""
    st.title("Login")
    
    with st.form("login_form", clear_on_submit=False):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        oauth_token = st.text_input("Google OAuth Token (Optional)")
        submit = st.form_submit_button("Login")

    if submit:
        # Validate email using email-validator
        try:
            validate_email(email)
        except EmailNotValidError as e:
            st.error(f"Invalid email: {str(e)}")
            return

        # Validate that the password field is not empty
        if not password:
            st.error("Password cannot be empty")
            return

        # Attempt to login
        result = attempt_login(email, password, oauth_token)
        
        if result.get("success"):
            st.success("Login successful!")
            # Store the token in session state
            st.session_state['jwt_token'] = result.get("token")
        else:
            st.error(f"Login failed: {result.get('error')}")


if __name__ == "__main__":
    login()
