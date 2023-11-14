#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of rss-reader
# https://github.com/scorphus/rss-reader

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2023, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# pylint: disable=line-too-long,missing-function-docstring,missing-module-docstring

import os

from setuptools import find_packages, setup


def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames), encoding="utf-8") as f:
        return f.read()


tests_require = [
    "autopep8",
    "black",
    "coverage",
    "factory-boy",
    "flake8",
    "httpx",
    "ipdb",
    "isort",
    "mypy",
    "pylint",
    "pytest-cov",
    "pytest-env",
    "pytest-mock",
    "pytest",
    "requests",
]

mypy_require = [
    "types-colorama",
    "types-pygments",
    "types-setuptools",
    "types-ujson",
]

setup(
    name="rss-reader",
    version="0.0.1",
    url="https://github.com/scorphus/rss-reader",
    license="BSD-3-Clause",
    description="rss-reader - RSS Reader",
    keywords="rss feed post reader",
    long_description=read("README.md"),
    classifiers=[
        "License :: OSI Approved :: 3-Clause BSD License License",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    author="Pablo S Blum de Aguiar",
    author_email="scorphus@gmail.com",
    packages=find_packages(),
    install_requires=[
        "FastAPI",  # web framework for building APIs (https://github.com/tiangolo/fastapi)
        "Feedparser",  # RSS feed parser (https://github.com/kurtmckee/feedparser)
        "Psycopg2-binary",  # PostgreSQL database adapter (https://github.com/psycopg/psycopg2)
        "Redis[hiredis]",  # interface to the Redis key-value store (https://github.com/redis/redis-py)
        "SQLmodel",  # library for interacting with SQL databases (https://github.com/tiangolo/sqlmodel)
        "uvicorn[standard]",  # ASGI server (https://github.com/encode/uvicorn)
    ],
    extras_require={
        "tests": tests_require,
        "mypy": mypy_require,
    },
    entry_points={
        "console_scripts": [
            "rss-reader = rss_reader.console:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
