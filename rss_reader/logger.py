#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of rss-reader
# https://github.com/scorphus/rss-reader

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2023, Pablo S. Blum de Aguiar <scorphus@gmail.com>

"""logger defines the logger for the application"""

import logging
import os


try:
    import logtail
except ImportError:
    logtail = None

LOG_LEVEL = os.getenv("LOG_LEVEL", "ERROR")
LOGTAIL_HANDLER_SOURCE_TOKEN = os.getenv("LOGTAIL_HANDLER_SOURCE_TOKEN", None)

logging_level = getattr(logging, LOG_LEVEL, logging.ERROR)
logging.basicConfig(level=logging_level, format="%(asctime)s %(levelname)-8s %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging_level)

if logtail and LOGTAIL_HANDLER_SOURCE_TOKEN:
    logger.addHandler(logtail.LogtailHandler(source_token=LOGTAIL_HANDLER_SOURCE_TOKEN))
