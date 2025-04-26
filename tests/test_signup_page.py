import os
import json
import requests
import pytest

from demo5_web_svc.pages import signup


class DummyResponse:
    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self._json = json_data

    def json(self):
        return self._json

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"HTTP {self.status_code}")


# Tests for validate_inputs

def test_validate_inputs_valid():
    valid, msg = signup.validate_inputs("test@example.com", "strongpassword", "valid_token")
    assert valid
    assert msg == ""


def test_validate_inputs_invalid_email():
    valid, msg = signup.validate_inputs("invalid-email", "strongpassword", "valid_token")
    assert not valid
    assert "Invalid email" in msg


def test_validate_inputs_short_password():
    valid, msg = signup.validate_inputs("test@example.com", "short", "valid_token")
    assert not valid
    assert msg == "Password must be at least 8 characters long."


def test_validate_inputs_empty_oauth_token():
    valid, msg = signup.validate_inputs("test@example.com", "strongpassword", "")
    assert not valid
    assert msg == "Google OAuth token/authorization code is required."


# Tests for perform_signup_request

def test_perform_signup_request_success(monkeypatch):
    # Dummy successful response
    def dummy_post(url, json, headers, timeout):
        return DummyResponse(200, {"jwt_token": "dummy_jwt_token"})

    monkeypatch.setattr("requests.post", dummy_post)
    success, token = signup.perform_signup_request("test@example.com", "strongpassword", "valid_token")
    assert success
    assert token == "dummy_jwt_token"


def test_perform_signup_request_failure(monkeypatch):
    # Dummy failure response (no jwt_token in json)
    def dummy_post(url, json, headers, timeout):
        return DummyResponse(200, {"error": "failure"})

    monkeypatch.setattr("requests.post", dummy_post)
    success, message = signup.perform_signup_request("test@example.com", "strongpassword", "valid_token")
    assert not success
    assert "JWT token not received" in message


def test_perform_signup_request_exception(monkeypatch):
    # Simulate exception during request
    def dummy_post(url, json, headers, timeout):
        raise requests.RequestException("Network error")

    monkeypatch.setattr("requests.post", dummy_post)
    success, message = signup.perform_signup_request("test@example.com", "strongpassword", "valid_token")
    assert not success
    assert "Signup error:" in message
