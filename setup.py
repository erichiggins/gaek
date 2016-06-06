#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup
from setuptools import find_packages

# https://bugs.python.org/issue15881
try:
  import multiprocessing
except ImportError:
  pass


def readme():
  with open('README.md') as fp:
    return fp.read()


def version():
  with open('VERSION') as fp:
    return fp.readline().rstrip('\n')


def requirements():
  with open('requirements.txt') as fp:
    return fp.read()


def test_requirements():
  with open('requirements_test.txt') as fp:
    return fp.read()


setup(
    name='gaek',
    version=version(),
    description="A collection of useful tools for Python apps running on Google App Engine.",
    long_description=readme(),
    author="Eric Higgins",
    author_email='erichiggins@gmail.com',
    url='https://github.com/erichiggins/gaek',
    license="BSD",
    packages=find_packages(exclude=['tests', 'google']),
    include_package_data=True,
    install_requires=requirements(),
    test_suite='tests',
    tests_require=test_requirements(),
    zip_safe=False)
