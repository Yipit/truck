#!/usr/bin/env python
# -*- coding: utf-8 -*-

from truck.conf import LISTENERS_OFF_BY_DEFAULT
from truck import Loader


if not LISTENERS_OFF_BY_DEFAULT:
    Loader.start()
