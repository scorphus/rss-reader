#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of rss-reader
# https://github.com/scorphus/rss-reader

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2023, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# pylint: disable=missing-function-docstring,missing-module-docstring
# pylint: disable=redefined-outer-name,unused-argument

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from rss_reader import db


@pytest.fixture(name="replenish_mock", autouse=True)
def replenish_mock_fixture(mocker):
    return mocker.patch("rss_reader.feedsvc.replenish")


@pytest.mark.parametrize(
    "username",
    [
        "joe",
        "Joe",
        "joe1",
        "joe_1",
        "___",
    ],
)
def test_create_user(username: str, client: TestClient):
    response = client.post("/users/", json={"username": username})
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == username
    assert data["id"] is not None


@pytest.mark.parametrize(
    "username",
    [
        "",
        " ",
        "  ",
        "   ",
        "\n",
        "\n\n",
        "\n\n\n",
        " \n",
        " \n\n",
        "joe ",
        " joe",
        " joe\n",
        "joe-1",
        "joe.1",
        "joe_1.1",
        "joe-1.1",
        "joe.1-1",
        "joe_1-1",
        "joe-1_1",
        "joe.1_1",
    ],
)
def test_create_user_invalid(username: str, client: TestClient):
    response = client.post("/users/", json={"username": username})
    assert response.status_code == 422


def test_create_user_dupe(client: TestClient):
    response = client.post("/users/", json={"username": "donna"})
    assert response.status_code == 201
    response = client.post("/users/", json={"username": "donna"})
    assert response.status_code == 409


def test_read_users(reset_db: db.Engine, client: TestClient):
    client.post("/users/", json={"username": "user_1"})
    client.post("/users/", json={"username": "user_2"})
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["username"] == "user_1"
    assert data[1]["username"] == "user_2"


def test_read_users_empty_db(reset_db: db.Engine, client: TestClient):
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0


def test_read_user(client: TestClient):
    client.post("/users/", json={"username": "dan"})
    response = client.get("/users/dan")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "dan"


def test_read_user_not_found(client: TestClient):
    response = client.get("/users/notdan")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_read_user_not_found_no_route(client: TestClient):
    response = client.get("/users/dan/wannabe")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_update_user(session: Session, client: TestClient):
    response = client.post("/users/", json={"username": "dave"})
    data = response.json()
    user_id = data["id"]
    response = client.patch("/users/dave", json={"username": "david"})
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == user_id
    assert data["username"] == "david"
    response = client.get("/users/david")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "david"
    assert data["id"] == user_id
    response = client.get("/users/dave")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_update_user_not_found(client: TestClient):
    response = client.patch("/users/notdave", json={"username": "david"})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_update_user_existing(client: TestClient):
    client.post("/users/", json={"username": "jack"})
    client.post("/users/", json={"username": "daniels"})
    response = client.patch("/users/daniels", json={"username": "jack"})
    assert response.status_code == 409
    response = client.get("/users/daniels")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "daniels"


def test_update_user_invalid(client: TestClient):
    client.post("/users/", json={"username": "john"})
    response = client.patch("/users/john", json={"username": "john daniels"})
    assert response.status_code == 422


def test_delete_user(client: TestClient):
    response = client.post("/users/", json={"username": "bruce"})
    data = response.json()
    user_id = data["id"]
    response = client.get("/users/bruce")
    assert response.status_code == 200
    response = client.delete("/users/bruce")
    assert response.status_code == 204
    response = client.get("/users/bruce")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
    response = client.get("/users/")
    data = response.json()
    assert user_id not in [user["id"] for user in data]


def test_delete_user_not_found(client: TestClient):
    response = client.delete("/users/notbruce")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_delete_user_no_username_not_allowed(client: TestClient):
    response = client.delete("/users/")
    assert response.status_code == 405
    assert response.json() == {"detail": "Method Not Allowed"}


def test_create_feed(client: TestClient):
    response = client.post("/feeds/", json={"url": "http://feed1.com"})
    assert response.status_code == 201
    data = response.json()
    assert data["url"] == "http://feed1.com"
    assert not data["title"]
    assert not data["subtitle"]
    assert not data["updated"]


def test_create_feed_invalid(client: TestClient):
    response = client.post("/feeds/", json={"url": "feed1.com"})
    assert response.status_code == 422


def test_create_feed_dupe(client: TestClient):
    response = client.post("/feeds/", json={"url": "http://feed2.com"})
    assert response.status_code == 201
    response = client.post("/feeds/", json={"url": "http://feed2.com"})
    assert response.status_code == 409


def test_read_feeds(reset_db: db.Engine, client: TestClient):
    client.post("/feeds/", json={"url": "http://feed3.com"})
    client.post("/feeds/", json={"url": "http://feed4.com"})
    response = client.get("/feeds/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["url"] == "http://feed3.com"
    assert data[1]["url"] == "http://feed4.com"


def test_read_feeds_empty_db(reset_db: db.Engine, client: TestClient):
    response = client.get("/feeds/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0


def test_read_feed(client: TestClient):
    response = client.post("/feeds/", json={"url": "http://feed5.com"})
    data = response.json()
    feed_id = data["id"]
    response = client.get(f"/feeds/{feed_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["url"] == "http://feed5.com"


def test_read_feed_not_found(client: TestClient):
    response = client.get("/feeds/123")
    assert response.status_code == 404
    assert response.json() == {"detail": "Feed not found"}


def test_read_feed_not_found_no_route(client: TestClient):
    response = client.get("/feeds/123/wannabe")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_delete_feed(client: TestClient):
    response = client.post("/feeds/", json={"url": "http://feed6.com"})
    data = response.json()
    feed_id = data["id"]
    response = client.get(f"/feeds/{feed_id}")
    assert response.status_code == 200
    response = client.delete(f"/feeds/{feed_id}")
    assert response.status_code == 204
    response = client.get(f"/feeds/{feed_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Feed not found"}
    response = client.get("/feeds/")
    data = response.json()
    assert feed_id not in [feed["id"] for feed in data]


def test_delete_feed_not_found(client: TestClient):
    response = client.delete("/feeds/123")
    assert response.status_code == 404
    assert response.json() == {"detail": "Feed not found"}


def test_delete_feed_no_feed_id_not_allowed(client: TestClient):
    response = client.delete("/feeds/")
    assert response.status_code == 405
    assert response.json() == {"detail": "Method Not Allowed"}
