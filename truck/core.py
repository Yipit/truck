#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
