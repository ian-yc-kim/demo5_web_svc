import importlib
import streamlit as st
import pytest

import demo5_web_svc.app as app


def test_signup_navigation(monkeypatch):
    # Flag to verify that render_signup_page is called
    called = {"value": False}
    
    # Patch the signup page render function
    from demo5_web_svc.pages import signup
    monkeypatch.setattr(signup, "render_signup_page", lambda: called.update({"value": True}))
    
    # Patch the sidebar radio to return "Signup"
    monkeypatch.setattr(st.sidebar, "radio", lambda label, options: "Signup")
    
    # Reload the app to trigger the navigation logic
    importlib.reload(app)
    
    assert called["value"] is True


def test_login_navigation(monkeypatch):
    called = {"value": False}
    
    # Patch the login function
    from demo5_web_svc.pages import login
    monkeypatch.setattr(login, "login", lambda: called.update({"value": True}))
    
    # Patch the sidebar radio to return "Login"
    monkeypatch.setattr(st.sidebar, "radio", lambda label, options: "Login")
    
    importlib.reload(app)
    
    assert called["value"] is True


def test_forum_navigation(monkeypatch):
    called = {"value": False}
    
    # Patch the forum page render function
    from demo5_web_svc.pages import forum
    monkeypatch.setattr(forum, "render_forum_page", lambda: called.update({"value": True}))
    
    # Patch the sidebar radio to return "Forum"
    monkeypatch.setattr(st.sidebar, "radio", lambda label, options: "Forum")
    
    importlib.reload(app)
    
    assert called["value"] is True


def test_meetings_navigation(monkeypatch):
    called = {"value": False}
    
    # Patch the meeting appointment page render function
    from demo5_web_svc.pages import meeting_appointment
    monkeypatch.setattr(meeting_appointment, "render_meeting_appointment_page", lambda: called.update({"value": True}))
    
    # Patch the sidebar radio to return "Meetings"
    monkeypatch.setattr(st.sidebar, "radio", lambda label, options: "Meetings")
    
    importlib.reload(app)
    
    assert called["value"] is True
