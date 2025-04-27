import json
import requests
import logging
import pytest

from demo5_web_svc.pages.meeting_appointment import create_meeting, fetch_meetings


class FakeResponse:
    def __init__(self, status_code: int, json_data=None, text: str = ""):
        self.status_code = status_code
        self._json = json_data
        self.text = text

    def json(self):
        return self._json


def fake_post_success(url, json, headers):
    return FakeResponse(201, json_data={"id": 1, "time": json.get("time"), "location": json.get("location"), "participants": json.get("participants")}, text="Created")


def fake_post_failure(url, json, headers):
    return FakeResponse(400, json_data=None, text="Bad Request")


def fake_get_success(url):
    data = [
        {"time": "2023-12-31T10:00:00", "location": "Conference Room", "participants": ["user@example.com"]}
    ]
    return FakeResponse(200, json_data=data, text="OK")


def fake_get_failure(url):
    return FakeResponse(500, json_data=None, text="Internal Server Error")


def test_create_meeting_success(monkeypatch):
    monkeypatch.setattr(requests, "post", fake_post_success)
    payload = {
        "time": "2099-01-01T10:00:00",
        "location": "Main Hall",
        "participants": ["user1@example.com", "user2@example.com"]
    }
    success, message = create_meeting(payload)
    assert success is True
    assert "successfully" in message


def test_create_meeting_failure(monkeypatch):
    monkeypatch.setattr(requests, "post", fake_post_failure)
    payload = {
        "time": "2099-01-01T10:00:00",
        "location": "",
        "participants": []
    }
    success, message = create_meeting(payload)
    assert success is False
    assert "Failed to create meeting" in message


def test_fetch_meetings_success(monkeypatch):
    monkeypatch.setattr(requests, "get", fake_get_success)
    success, data = fetch_meetings()
    assert success is True
    assert isinstance(data, list)
    assert len(data) > 0


def test_fetch_meetings_failure(monkeypatch):
    monkeypatch.setattr(requests, "get", fake_get_failure)
    success, message = fetch_meetings()
    assert success is False
    assert "Failed to fetch meetings" in message
