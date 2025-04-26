import requests
import streamlit as st
import pytest
from demo5_web_svc.pages import forum


class DummyResponse:
    def __init__(self, json_data, status_code):
        self._json_data = json_data
        self.status_code = status_code

    def json(self):
        return self._json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"HTTP {self.status_code} Error")


# Fixture to simulate authenticated session
@pytest.fixture(autouse=True)
def auth_token(monkeypatch):
    st.session_state.jwt_token = "dummy_token"
    return st.session_state.jwt_token


def test_fetch_posts_success(monkeypatch):
    dummy_posts = [{"id": 1, "title": "Test Post", "content": "Test Content"}]

    def dummy_get(url, headers):
        return DummyResponse(dummy_posts, 200)

    monkeypatch.setattr(requests, "get", dummy_get)
    posts = forum.fetch_posts("dummy_token")
    assert posts == dummy_posts


def test_fetch_posts_failure(monkeypatch):
    def dummy_get(url, headers):
        return DummyResponse({}, 500)

    monkeypatch.setattr(requests, "get", dummy_get)
    posts = forum.fetch_posts("dummy_token")
    # Verify that on error, empty list is returned
    assert posts == []


def test_create_post_success(monkeypatch):
    def dummy_post(url, json, headers):
        return DummyResponse({}, 200)

    monkeypatch.setattr(requests, "post", dummy_post)
    result = forum.create_post("dummy_token", "Title", "Content")
    assert result is True


def test_create_post_failure(monkeypatch):
    def dummy_post(url, json, headers):
        return DummyResponse({}, 500)

    monkeypatch.setattr(requests, "post", dummy_post)
    result = forum.create_post("dummy_token", "Title", "Content")
    assert result is False


def test_update_post_success(monkeypatch):
    def dummy_put(url, json, headers):
        return DummyResponse({}, 200)

    monkeypatch.setattr(requests, "put", dummy_put)
    result = forum.update_post("dummy_token", 1, "New Title", "New Content")
    assert result is True


def test_update_post_failure(monkeypatch):
    def dummy_put(url, json, headers):
        return DummyResponse({}, 500)

    monkeypatch.setattr(requests, "put", dummy_put)
    result = forum.update_post("dummy_token", 1, "New Title", "New Content")
    assert result is False


def test_delete_post_success(monkeypatch):
    def dummy_delete(url, headers):
        return DummyResponse({}, 200)

    monkeypatch.setattr(requests, "delete", dummy_delete)
    result = forum.delete_post("dummy_token", 1)
    assert result is True


def test_delete_post_failure(monkeypatch):
    def dummy_delete(url, headers):
        return DummyResponse({}, 500)

    monkeypatch.setattr(requests, "delete", dummy_delete)
    result = forum.delete_post("dummy_token", 1)
    assert result is False


def test_paginate_posts():
    # Create a dummy list of posts
    posts = [{'id': i, 'title': f'Title {i}', 'content': f'Content {i}'} for i in range(1, 11)]
    # Assuming POSTS_PER_PAGE is 5, page 2 should return posts 6-10
    page_number = 2
    paginated = forum.paginate_posts(posts, page_number)
    assert len(paginated) == 5
    assert paginated[0]['id'] == 6
    assert paginated[-1]['id'] == 10
