#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of truck
# <truck - test-friendly event bus layer on top of django signals>
# Copyright (C) <2012>  Gabriel Falcão <gabriel@yipit.com>
# Copyright (C) <2012>  Yipit Inc. <coders@yipit.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import imp
import logging
import importlib

from django.conf import settings
logger = logging.getLogger('truck')


class Loader(object):

    @classmethod
    def import_listener_from_module(cls, app):
        """Given an application name and a module name, tries to find that
        module in the application."""

        related_name = 'listeners'

        try:
            app_path = importlib.import_module(app).__path__
        except AttributeError:
            return

        try:
            imp.find_module(related_name, app_path)

        except ImportError:
            return

        return importlib.import_module("%s.%s" % (app, related_name))

    @classmethod
    def start(cls):
        return map(cls.import_listener_from_module, settings.INSTALLED_APPS)
