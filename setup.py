#!/usr/bin/python3
# Copyright (c) 2015 Dario Rubattu
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from setuptools import find_packages
from setuptools import setup

setup(name='book',
	version='0.1',
	description='Testnet BTC book',
	author='Dario Rubattu',
	setup_requires='setuptools',
	author_email='dr@fake.com',
	package_dir={'':'library'},
	packages=['book']
)
