#!/usr/bin/env/python

"""
	Setup script for NDD
"""

from setuptools import setup

setup(
	name='ndd',
	author='Ben Johnson',
	author_email='ben@gophronesis.com',
	classifiers=[],
	description='Near Duplicate Detection',
	keywords=['ndd'],
	license='ALV2',
	packages=['ndd', 'ndd.convnet_resources'],
	version="0.0.1"
)

