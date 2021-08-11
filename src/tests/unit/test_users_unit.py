import json
from datetime import datetime

import pytest

import src.api.users


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
    def mock_get_user_by_id(user_id):
        return {
            "id": 1,
            "username": "jeffrey",
            "email": "jeffrey@testdriven.io",
            "created_date": datetime.now(),
        }

    monkeypatch.setattr(src.api.users, "get_user_by_id", mock_get_user_by_id)
    client = test_app.test_client()
    resp = client.get("/users/1")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert "jeffrey" in data["username"]
    assert "jeffrey@testdriven.io" in data["email"]


def test_single_user_incorrect_id(test_app, monkeypatch):
    def mock_get_user_by_id(user_id):
        return None

    monkeypatch.setattr(src.api.users, "get_user_by_id", mock_get_user_by_id)
    client = test_app.test_client()
    resp = client.get("/users/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "User 999 does not exist" in data["message"]


def test_all_users(test_app, monkeypatch):
    def mock_get_all_users():
        return [
            {
                "id": 1,
                "username": "michael",
                "email": "michael@mherman.org",
                "created_date": datetime.now(),
            },
            {
                "id": 1,
                "username": "fletcher",
                "email": "fletcher@notreal.com",
                "created_dated": datetime.now(),
            },
        ]

    monkeypatch.setattr(src.api.users, "get_all_users", mock_get_all_users)
    client = test_app.test_client()
    resp = client.get("/users")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data) == 2
    assert "michael" in data[0]["username"]
    assert "michael@mherman.org" in data[0]["email"]
    assert "fletcher" in data[1]["username"]
    assert "fletcher@notreal.com" in data[1]["email"]


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
