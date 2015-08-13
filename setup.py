#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# setup.py
# Python 2.7 client library for the Nimvelo/Sipcentric API
# Copyright (c) 2015 Sipcentric Ltd. Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php

import os
from setuptools import setup

setup(
    name='nimvelo',
    description='Python 2.7 client library for the Nimvelo/Sipcentric API',
    version='0.1.4',
    url='https://github.com/Nimvelo/python-client',
    author='David Maitland',
    author_email='david.maitland@nimvelo.com',
    license='MIT',
    keywords='nimvelo sipcentric voip pbx sms sip',
    packages=['nimvelo', 'nimvelo/stream'],
    requires=['math', 'json', 'logging', 'time', 'simplejson'],
    install_requires=['requests']
)
