#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of rss-reader
# https://github.com/scorphus/rss-reader

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2023, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# pylint: disable=missing-function-docstring,missing-module-docstring
# pylint: disable=redefined-outer-name,unused-argument

import functools
from unittest.mock import Mock

import feedparser
import pytest
from fastapi.testclient import TestClient


@pytest.fixture(name="feedparser_mock")
def feedparser_mock_fixture(request, mocker):
    fixture = request.param if hasattr(request, "param") else "programming.rss"
    with open(f"tests/fixtures/{fixture}", "rb") as file:
        yield mocker.patch(
            "rss_reader.feedsvc.feedparser.parse",
            side_effect=functools.partial(feedparser.parse, file),
        )


def test_create_feed_replenished(client: TestClient, feedparser_mock: Mock):
    url = "https://www.reddit.com/r/programming/.rss"
    response = client.post("/feeds/", json={"url": url})
    assert response.status_code == 201
    data = response.json()
    assert data["url"] == url
    assert data["title"] == "programming"
    assert data["subtitle"] == "Computer Programming"
    assert data["updated"] == "2023-11-16T13:54:19"
    feedparser_mock.assert_called_once_with(url)


@pytest.mark.parametrize("feedparser_mock", ["not_a_feed.rss"], indirect=True)
def test_create_feed_replenished_not_a_feed(client: TestClient, feedparser_mock: Mock):
    url = "https://some.url.com/"
    response = client.post("/feeds/", json={"url": url})
    assert response.status_code == 201
    data = response.json()
    assert data["url"] == url
    assert data["title"] == "No title (or not a RSS feed)"
    assert data["subtitle"] == "No subtitle"
    assert not data["updated"]


@pytest.mark.parametrize("feedparser_mock", ["404_error.rss"], indirect=True)
def test_create_feed_replenished_404_error(client: TestClient, feedparser_mock: Mock):
    url = "https://some.other.url.com/"
    response = client.post("/feeds/", json={"url": url})
    assert response.status_code == 201
    data = response.json()
    assert data["url"] == url
    assert data["title"] == "No title (or not a RSS feed)"
    assert data["subtitle"] == "No subtitle"
    assert not data["updated"]
