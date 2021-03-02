#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.read().splitlines()

setup(
    name='pepperboard',
    version='3.0',
    packages=['pepperboard', 'pepperboard.core', 'pepperboard.dashboards'],
    scripts=['scripts/pepperboard'],
    url='https://github.com/webedia-dev/pepperboard',
    download_url='https://github.com/webedia-dev/pepperboard/releases/tag/v3.0',
    license='Apache',
    author='Cyril LAVIER',
    author_email='cyril.lavier@webedia-group.com',
    description='Simple and modular dashboard toolkit for SaltStack',
    install_requires=requirements,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: System :: Monitoring',
    ],
)
