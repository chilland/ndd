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
	packages=['ndd'],
	version="0.0.2",
	install_requires=[
		"Keras==1.1.0",
		"numpy>=1.11.2",
		"scipy>=0.18.1",
		"redis==2.10.5",
		"redis-py-cluster==1.2.0"
	]
)