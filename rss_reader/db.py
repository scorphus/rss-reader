#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of rss-reader
# https://github.com/scorphus/rss-reader

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2023, Pablo S. Blum de Aguiar <scorphus@gmail.com>

"""Models definitions and database operations"""

import functools
import os
import urllib
from datetime import datetime
from typing import List, Optional

import sqlalchemy
from pydantic import validator
from sqlalchemy.future import Engine
from sqlmodel import Field, Session, SQLModel
from sqlmodel import create_engine as sqlmodel_create_engine
from sqlmodel import select

from rss_reader.logger import LOG_LEVEL, logger


DATABASE_URL = os.getenv(
    "RSS_READER_DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/rss_reader"
)


# class FeedUserSub(SQLModel, table=True):
#     """FeedUserSub defines the model of a feed subscription by a user"""

#     feed_id: Optional[int] = Field(default=None, foreign_key="feed.id", primary_key=True)
#     user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)


# class PostUserRead(SQLModel, table=True):
#     """PostUserRead defines the model of a post read by a user"""

#     post_id: Optional[int] = Field(default=None, foreign_key="post.id", primary_key=True)
#     user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)


# class Post(SQLModel, table=True):
#     """Post defines the model for a post"""

#     id: Optional[int] = Field(default=None, primary_key=True)
#     post_id: str = Field(sa_column_kwargs={"unique": True})
#     title: str
#     link: str
#     summary: str
#     published: datetime
#     feed_id: int = Field(foreign_key="feed.id")
#     feed: Feed = Relationship(back_populates="posts")
#     readers: List["User"] = Relationship(back_populates="read_posts", link_model=PostUserRead)

#     def __repr__(self) -> str:
#         return f"Post(post_id={self.post_id})"


class UserBase(SQLModel):
    """User defines the base model for a user"""

    username: str = Field(sa_column_kwargs={"unique": True}, index=True, min_length=2)
    # subscriptions: List[Feed] = Relationship(back_populates="subscribers", link_model=FeedUserSub)
    # read_posts: List[Post] = Relationship(back_populates="readers", link_model=PostUserRead)

    @validator("username")
    def valid_username(cls, value: str) -> str:  # pylint: disable=no-self-argument
        """Validate username"""
        assert value.isidentifier(), "must consist of alphanumeric characters and underscores"
        return value

    def __repr__(self) -> str:
        return f"User(username={self.username})"


class User(UserBase, table=True):
    """User defines the full model for a user"""

    id: Optional[int] = Field(default=None, primary_key=True)


class FeedBase(SQLModel):
    """Feed defines the base model for a feed"""

    url: str = Field(sa_column_kwargs={"unique": True})

    @validator("url")
    def valid_url(cls, value: str) -> str:  # pylint: disable=no-self-argument
        """Validate url"""
        assert urllib.parse.urlparse(value).scheme in {"http", "https"}, "must be a valid URL"
        return value

    def __repr__(self) -> str:
        return f"Feed(url={self.url})"


class Feed(FeedBase, table=True):
    """Feed defines the full model for a feed"""

    id: Optional[int] = Field(default=None, primary_key=True)
    title: Optional[str]
    subtitle: Optional[str]
    updated: Optional[datetime]
    # posts: List["Post"] = Relationship(back_populates="feed")
    # subscribers: List["User"] = Relationship(
    #     back_populates="subscriptions", link_model=FeedUserSub
    # )


@functools.cache
def create_engine(database_url: str = DATABASE_URL) -> Engine:
    """Create the database engine"""
    logger.debug("Creating engine with url %s", database_url)
    return sqlmodel_create_engine(database_url, echo=LOG_LEVEL == "DEBUG")


def create_tables(engine: Engine) -> None:
    """Create all tables in the database"""
    SQLModel.metadata.create_all(engine)


def drop_tables(engine: Engine) -> None:
    """Drop all tables in the database"""
    SQLModel.metadata.drop_all(engine)


def add_user(session: Session, user: User) -> User:
    """Add a user to the database"""
    try:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    except sqlalchemy.exc.IntegrityError as err:
        session.rollback()
        raise ValueError("User already exists") from err


def get_users(session: Session, offset: int = 0, limit: int = 10) -> List[User]:
    """Get all users from the database"""
    return session.exec(select(User).offset(offset).limit(limit)).all()


def get_user(session: Session, username: str) -> Optional[User]:
    """Get a user from the database"""
    return session.exec(select(User).where(User.username == username)).first()


def update_user(session: Session, username: str, user: UserBase) -> Optional[User]:
    """Update a user in the database"""
    existing_user = get_user(session, username)
    if not existing_user:
        return None
    for field, value in user.dict(exclude_unset=True).items():
        setattr(existing_user, field, value)
    try:
        session.add(existing_user)
        session.commit()
        session.refresh(existing_user)
        return existing_user
    except sqlalchemy.exc.IntegrityError as err:
        session.rollback()
        raise ValueError("User already exists") from err


def delete_user(session: Session, username: str) -> Optional[User]:
    """Delete a user from the database"""
    existing_user = get_user(session, username)
    if not existing_user:
        return None
    session.delete(existing_user)
    session.commit()
    return existing_user


def add_feed(session: Session, feed: Feed) -> Feed:
    """Add a feed to the database"""
    try:
        session.add(feed)
        session.commit()
        session.refresh(feed)
        return feed
    except sqlalchemy.exc.IntegrityError as err:
        session.rollback()
        raise ValueError("Feed already exists") from err


def get_feeds(session: Session, offset: int = 0, limit: int = 10) -> List[Feed]:
    """Get all feeds from the database"""
    return session.exec(select(Feed).offset(offset).limit(limit)).all()


def get_feed(session: Session, feed_id: int) -> Optional[Feed]:
    """Get a feed from the database"""
    return session.exec(select(Feed).where(Feed.id == feed_id)).first()


def delete_feed(session: Session, feed_id: int) -> Optional[Feed]:
    """Delete a feed from the database"""
    existing_feed = get_feed(session, feed_id)
    if not existing_feed:
        return None
    session.delete(existing_feed)
    session.commit()
    return existing_feed
