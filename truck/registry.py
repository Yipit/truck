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

from truck.core import Loader
signal_registry = []


def connect_all_signals():
    Loader.start()
    for (signal, listener, args, kw) in signal_registry:
        signal.connect(listener, *args, **kw)


def disconnect_all_signals():
    for (signal, listener, args, kw) in signal_registry:
        signal.disconnect(listener, *args, **kw)
