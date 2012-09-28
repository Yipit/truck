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
version = '0.1.3'

from functools import wraps
from django.dispatch import receiver as signal_receiver
from truck.core import Loader
from truck.conf import LISTENERS_OFF_BY_DEFAULT
from truck.registry import (
    connect_all_signals,
    disconnect_all_signals,
    signal_registry,
)


__all__ = ['Loader', 'receiver', 'connect_signal', 'truck_enabled']


def receiver(signal, *args, **kw):
    """Decorator for attaching signal receivers
    to the internal pool of signal receivers within django

    It's pretty much a wrapper around the
    `from django.dispatch import receiver` decorator
    The only difference is that the decorated function will never
    be considered a signal listener within automated tests
    (a.k.a. settings.TESTING=True)

    Usage:

    in your {app}/listeners.py

    >>> from truck import receiver
    >>> from some_app.signals import signal_name
    >>>
    >>> @receiver(signal_name)
    ... def do_some_action(sender, **kwargs):
    ...     pass

    """

    def wrapper(function):
        if 'sender' in kw:
            raise TypeError(
                "Listeners to custom signals should not specify sender. {}, line: {}".format(
                    function.func_code.co_filename, function.func_code.co_firstlineno
                )
            )

        if not LISTENERS_OFF_BY_DEFAULT:
            connected = signal_receiver(signal, *args, **kw)
            return connected(function)
        else:
            signal_registry.append((signal, function, args, kw))
            return function

    return wrapper


def connect_signal(signal, listener, *args, **kw):
    """helper function for connecting django signals to listeners with
    a simple check to avoid it to happen when running tests.

    Use where you would use signal.connect.

    For example, instead of doing:

    >>> from deal.models import Deal
    >>> from django.db.models.signals import post_save
    >>> def my_listener(sender, instance, **kw):
    ...     redis.sadd('yipit:deals', instance.id)
    ...
    >>> post_save.connect(my_listener, sender=Deal)

    you should rather use:

    >>> import truck
    >>> truck.connect_signal(post_save, my_listener, sender=Deal)

    It will protect the listener to be triggered, for instance, within
    unit and functional tests
    """
    if LISTENERS_OFF_BY_DEFAULT:
        signal_registry.append((signal, listener, args, kw))
        # never connect signals in tests
        return

    return signal.connect(listener, *args, **kw)


def truck_enabled(func):
    @wraps(func)
    def wrapper(*args, **kw):
        connect_all_signals()
        try:
            ret = func(*args, **kw)
        except Exception:
            disconnect_all_signals()
            raise

        disconnect_all_signals()

        return ret

    return wrapper
