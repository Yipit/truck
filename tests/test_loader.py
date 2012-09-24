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

from mock import patch, call
from truck.core import Loader


@patch('truck.core.importlib')
@patch('truck.core.imp')
def test_loader_should_be_able_to_load_a_single_module(imp, importlib):
    u"Loader should be able to load a listener from a module"
    importlib.import_module.return_value.__path__ = '/some/path'

    Loader.import_listener_from_module('deal')

    imp.find_module.assert_called_once_with('listeners', '/some/path')
    importlib.import_module.assert_has_calls([
        call('deal'),
        call('deal.listeners'),
    ])


@patch('truck.core.importlib')
@patch('truck.core.imp')
def test_loader_should_ignore_if_there_is_no_such_app(imp, importlib):
    "Loader should ignore when the app does not exist"
    importlib.import_module.side_effect = (
        AttributeError('there is no such module'))

    Loader.import_listener_from_module('deal')
    importlib.import_module.assert_called_once_with('deal')
    assert not imp.find_module.called


@patch('truck.core.importlib')
@patch('truck.core.imp')
def test_loader_should_ignore_if_there_are_no_listeners(imp, importlib):
    "Loader should ignore when the app does not exist"
    importlib.import_module.return_value.__path__ = '/some/path'
    imp.find_module.side_effect = ImportError('LOL')

    Loader.import_listener_from_module('deal')

    importlib.import_module.assert_called_once_with('deal')
    imp.find_module.assert_called_once_with('listeners', '/some/path')


@patch.object(Loader, 'import_listener_from_module')
@patch('truck.core.settings')
def test_loader_start_maps_installed_apps(
    settings, import_listener_from_module):
    "Loader.start() should ignore when the app does not exist"

    settings.INSTALLED_APPS = ['chuck', 'norris']

    Loader.start()

    import_listener_from_module.assert_has_calls([
        call('chuck'),
        call('norris'),
    ])
