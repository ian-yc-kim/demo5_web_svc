import requests

from demo5_web_svc.pages import login
from demo5_web_svc import config


class FakeResponse:
    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self._json = json_data

    def json(self):
        return self._json


def test_attempt_login_success(monkeypatch):
    def fake_post(url, json, headers, timeout):
        expected_url = f"{config.AUTH_SERVICE_URL}/api/login"
        assert url == expected_url
        assert headers == {"Content-Type": "application/json"}
        expected_payload = {"email": "user@example.com", "password": "password123", "oauth_token": "tokenX"}
        assert json == expected_payload
        return FakeResponse(200, {"token": "jwt_token_value"})

    monkeypatch.setattr(requests, "post", fake_post)
    result = login.attempt_login("user@example.com", "password123", "tokenX")
    assert result.get("success") is True
    assert result.get("token") == "jwt_token_value"


def test_attempt_login_failure(monkeypatch):
    def fake_post(url, json, headers, timeout):
        return FakeResponse(401, {"error": "Invalid credentials"})

    monkeypatch.setattr(requests, "post", fake_post)
    result = login.attempt_login("user@example.com", "wrongpassword", "")
    assert result.get("success") is False
    assert result.get("error") == "Invalid credentials"


def test_attempt_login_exception(monkeypatch):
    def fake_post(url, json, headers, timeout):
        raise Exception("Network error")

    monkeypatch.setattr(requests, "post", fake_post)
    result = login.attempt_login("user@example.com", "password", "")
    assert result.get("success") is False
    assert result.get("error") == "Request failed"
