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


@app.patch("/users/{username}")
def update_user(
    *,
    session: db.Session = Depends(get_session),
    username: str,
    user: db.UserBase,
) -> db.User:
    """Update a user"""
    try:
        updated_user = db.update_user(session, username=username, user=user)
    except ValueError as err:
        raise HTTPException(status_code=409, detail=str(err)) from err
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@app.delete("/users/{username}", status_code=204)
def delete_user(*, session: db.Session = Depends(get_session), username: str) -> None:
    """Delete a user"""
    user = db.delete_user(session, username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")


@app.post("/feeds/", status_code=201)
def create_feed(*, session: db.Session = Depends(get_session), feed: db.FeedBase) -> db.Feed:
    """Create a new feed"""
    new_feed = db.Feed.from_orm(feed)
    try:
        return db.add_feed(session, new_feed)
    except ValueError as err:
        raise HTTPException(status_code=409, detail=str(err)) from err


@app.get("/feeds/")
def read_feeds(
    *,
    session: db.Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
) -> List[db.Feed]:
    """Return a list of feeds"""
    return db.get_feeds(session, offset=offset, limit=limit)


@app.get("/feeds/{feed_id}")
def read_feed(*, session: db.Session = Depends(get_session), feed_id: int) -> db.Feed:
    """Return a feed"""
    feed = db.get_feed(session, feed_id=feed_id)
    if not feed:
        raise HTTPException(status_code=404, detail="Feed not found")
    return feed
