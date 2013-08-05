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
from mock import patch
from sure import expect
from setup import version as setup_version
from truck import version as core_version

from truck import conf


def test_version_matches():
    ("the version in setup.py and in the core module should match")
    expect(core_version).to.equal(setup_version)


@patch('truck.conf.settings')
def test_conf_no_testing_var(settings):
    ("truck should not disable listeners when not testing")

    # Given that I'm not in the testing environment
    delattr(settings, 'TESTING')

    # When I query the conf submodule
    conf.LISTENERS_OFF_BY_DEFAULT.should.be.false


@patch('truck.conf.settings')
def test_conf_testing_unit(settings):
    ("truck should not disable listeners when not testing")

    # Given that I'm not in the testing environment
    setattr(settings, 'TESTING', 'unit')

    # When I query the conf submodule
    conf.LISTENERS_OFF_BY_DEFAULT.should.be.true


@patch('truck.conf.settings')
def test_conf_testing_acceptance(settings):
    ("truck should not disable listeners on acceptance tests")

    # Given that I'm not in the testing environment
    setattr(settings, 'TESTING', 'acceptance')

    # When I query the conf submodule
    conf.LISTENERS_OFF_BY_DEFAULT.should.be.false
