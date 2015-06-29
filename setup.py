#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup
from setuptools import find_packages


with open('VERSION') as version_file:
    VERSION = version_file.readline().rstrip('\n')

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.read()

with open('test_requirements.txt') as test_requirements_file:
    test_requirements = test_requirements_file.read()

setup(
    name='gaek',
    version=VERSION,
    description="A collection of useful tools for Python apps running on Google App Engine.",
    author="Eric Higgins",
    author_email='erichiggins@gmail.com',
    url='https://github.com/erichiggins/gaek',
    packages=find_packages(exclude=['tests']),
    install_requires=requirements,
    license="BSD",
    keywords='gaek',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
