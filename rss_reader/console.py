#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of rss-reader
# https://github.com/scorphus/rss-reader

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2023, Pablo S. Blum de Aguiar <scorphus@gmail.com>

"""This module provides the `rss_reader` console utility"""

import argparse
import sys

from rss_reader import db


def main():
    """Defines argument parser and runs the proper action"""
    parser = argparse.ArgumentParser(description="rss_reader console utility")
    parser.add_argument(
        "-d",
        "--database-url",
        type=str,
        default=db.DATABASE_URL,
        help="The URL of the rss_reader database [default: %(default)s]",
    )
    parser.add_argument(
        "action",
        type=str,
        choices=["create-tables", "drop-tables"],
        help="The action to be performed",
    )
    arguments = parser.parse_args(sys.argv[1:])
    match arguments.action:
        case "create-tables":
            engine = db.create_engine(arguments.database_url)
            db.create_tables(engine)
        case "drop-tables":
            engine = db.create_engine(arguments.database_url)
            db.drop_tables(engine)
        case _:
            parser.print_help()
