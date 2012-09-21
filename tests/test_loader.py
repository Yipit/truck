# -*- coding: utf-8 -*-

import os
import sys

test_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(test_dir, os.path.pardir))
os.environ["DJANGO_SETTINGS_MODULE"] = 'settings'

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
