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


class UserBase(SQLModel):
    """User defines the base model for a user"""

    username: str = Field(sa_column_kwargs={"unique": True}, index=True, min_length=2)

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
