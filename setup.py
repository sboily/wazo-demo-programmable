#!/usr/bin/env python3
# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from setuptools import setup
from setuptools import find_packages


NAME = 'wazo-demo-programmable'
setup(
    name=NAME,
    version='1.0',
    author='Wazo Authors',
    author_email='dev@wazo.community',
    url='http://wazo.community',
    packages=find_packages(),
    package_data={'wazo_demo_programmable.plugins': ['*/api.yml']},
    entry_points={
        'console_scripts': [
            '{}=wazo_demo_programmable.main:main'.format(NAME),
        ],
        'wazo_demo_programmable.plugins': [
            'auth = wazo_demo_programmable.plugins.auth.plugin:Plugin',
            'config = wazo_demo_programmable.plugins.config.plugin:Plugin',
            'call = wazo_demo_programmable.plugins.call.plugin:Plugin',
        ],
    },
)
