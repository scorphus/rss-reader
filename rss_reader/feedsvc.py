#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of rss-reader
# https://github.com/scorphus/rss-reader

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2023, Pablo S. Blum de Aguiar <scorphus@gmail.com>

"""Feed Service module"""

import feedparser

from rss_reader.db import Feed


def replenish(feed: Feed) -> None:
    """Replenish the feed with missing attributes"""
    parsed = feedparser.parse(feed.url)
    feed.title = parsed.feed.get("title", "No title (or not a RSS feed)")
    feed.subtitle = parsed.feed.get("subtitle", "No subtitle")
    feed.updated = parsed.feed.get("updated", None)
