#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings

LISTENERS_OFF_BY_DEFAULT = settings.TESTING and not settings.ACCEPTANCE_TESTING
