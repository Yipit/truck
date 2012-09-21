#!/usr/bin/env python
# -*- coding: utf-8 -*-
from truck.core import Loader
signal_registry = []


def connect_all_signals():
    Loader.start()
    for (signal, listener, args, kw) in signal_registry:
        signal.connect(listener, *args, **kw)


def disconnect_all_signals():
    for (signal, listener, args, kw) in signal_registry:
        signal.disconnect(listener, *args, **kw)
