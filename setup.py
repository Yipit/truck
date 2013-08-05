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

version = '0.1.4'

import os
from setuptools import setup, find_packages

os.environ['DJANGO_SETTINGS_MODULE'] = 'setup'


if __name__ == '__main__':
    setup(
        name='truck',
        version=version,
        description='test-friendly event bus layer on top of django signals',
        author=u'Gabriel Falcao',
        author_email='gabriel@yipit.com',
        url='http://github.com/Yipit/truck',
        packages=find_packages(exclude=['*tests*']),
    )
