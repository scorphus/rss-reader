#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of rss-reader
# https://github.com/scorphus/rss-reader

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2023, Pablo S. Blum de Aguiar <scorphus@gmail.com>

"""API definition and endpoints"""

from typing import List

from fastapi import Depends, FastAPI, HTTPException, Query

from rss_reader import db


app = FastAPI()
engine = db.create_engine()


def get_session():
    """Return a database session, necessary for dependency injection"""
    with db.Session(engine) as session:
        yield session


@app.post("/users/", status_code=201)
def create_user(*, session: db.Session = Depends(get_session), user: db.UserBase) -> db.User:
    """Create a new user"""
    new_user = db.User.from_orm(user)
    try:
        return db.add_user(session, new_user)
    except ValueError as err:
        raise HTTPException(status_code=409, detail=str(err)) from err


@app.get("/users/")
def read_users(
    *,
    session: db.Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
) -> List[db.User]:
    """Return a list of users"""
    return db.get_users(session, offset=offset, limit=limit)


@app.get("/users/{username}")
def read_user(*, session: db.Session = Depends(get_session), username: str) -> db.User:
    """Return a user"""
    user = db.get_user(session, username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
