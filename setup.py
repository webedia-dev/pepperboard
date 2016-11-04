#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pypandoc

from setuptools import setup

readme = pypandoc.convert_file('README.md','rst')

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.read().splitlines()

setup(
    name='pepperboard',
    version='1',
    packages=['pepperboard', 'pepperboard.core', 'pepperboard.dashboards'],
    scripts=['scripts/pepperboard'],
    url='https://github.com/webedia-dev/pepperboard',
    license='Apache',
    author='Cyril LAVIER',
    author_email='cyril.lavier@webedia-group.com',
    description='Simple and modular dashboard toolkit for SaltStack',
    long_description=readme,
    install_requires=requirements,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: System :: Monitoring',
    ],
)