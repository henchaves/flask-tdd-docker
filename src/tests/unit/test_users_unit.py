import json

import pytest

import src.api.users

# from datetime import datetime




def test_add_user(test_app, monkeypatch):
    def mock_get_user_by_email(email):
        return None

    def mock_add_user(username, email):
        return True

    monkeypatch.setattr(src.api.users, "get_user_by_email", mock_get_user_by_email)
    monkeypatch.setattr(src.api.users, "add_user", mock_add_user)

    client = test_app.test_client()
    resp = client.post(
        "/users",
        data=json.dumps({"username": "michael", "email": "michael@testdriven.io"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert "michael@testdriven.io was added!" in data["message"]


def test_add_user_invalid_json_keys(test_app, monkeypatch):
    client = test_app.test_client()
    resp = client.post(
        "/users",
        data=json.dumps({"email": "john@testdriven.io"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_add_user_duplicate_email(test_app, monkeypatch):
    def mock_get_user_by_email(email):
        return True

    def mock_add_user(username, email):
        return True

    monkeypatch.setattr(src.api.users, "get_user_by_email", mock_get_user_by_email)
    monkeypatch.setattr(src.api.users, "add_user", mock_add_user)
    client = test_app.test_client()
    resp = client.post(
        "/users",
        data=json.dumps({"username": "michael", "email": "michael@testdriven.io"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Sorry. That email already exists." in data["message"]


def test_single_user(test_app, monkeypatch):
    pass


def test_single_user_incorrect_id(test_app, monkeypatch):
    pass


def test_all_users(test_app, monkeypatch):
    pass


def test_remove_user(test_app, monkeypatch):
    pass


def test_remove_user_incorrect_id(test_app, monkeypatch):
    pass


def test_update_user(test_app, monkeypatch):
    pass


@pytest.mark.parametrize(
    "user_id, payload, status_code, message",
    [
        [1, {}, 400, "Input payload validation failed"],
        [1, {"email": "me@testdriven.io"}, 400, "Input payload validation failed"],
        [
            999,
            {"username": "me", "email": "me@testdriven.io"},
            404,
            "User 999 does not exist",
        ],
    ],
)
def test_update_user_invalid(
    test_app, monkeypatch, user_id, payload, status_code, message
):
    pass


def test_update_user_duplicate_email(test_app, monkeypatch):
    pass
