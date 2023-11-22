#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of rss-reader
# https://github.com/scorphus/rss-reader

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2023, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# pylint: disable=missing-function-docstring,missing-module-docstring
# pylint: disable=redefined-outer-name,unused-argument

import os

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from rss_reader import api, db


DATABASE_URL = os.getenv(
    "RSS_READER_TEST_DATABASE_URL", "postgresql://postgres:postgres@localhost:5434/rss_reader_test"
)


@pytest.fixture(name="engine", scope="session")
def engine_fixture():
    test_engine = db.create_engine(DATABASE_URL)
    db.create_tables(test_engine)
    yield test_engine
    db.drop_tables(test_engine)
    test_engine.dispose()


@pytest.fixture(name="reset_db")
def reset_db_fixture(engine: db.Engine):
    db.drop_tables(engine)
    db.create_tables(engine)
    return engine


@pytest.fixture(name="session")
def session_fixture(engine: db.Engine):
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    api.app.dependency_overrides[api.get_session] = lambda: session
    yield TestClient(api.app)
    api.app.dependency_overrides.clear()
