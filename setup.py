#!/usr/bin/env python

from setuptools import setup

setup(
    # GETTING-STARTED: set your app name:
    name='cnto',
    # GETTING-STARTED: set your app version:
    version='1.0',
    # GETTING-STARTED: set your app description:
    description='OpenShift App',
    # GETTING-STARTED: set author name (your name):
    author='Supreme',
    # GETTING-STARTED: set author email (your email):
    author_email='sakkie99@gmail.com',
    # GETTING-STARTED: set author url (your url):
    url='http://carpenoctem.co',
    # GETTING-STARTED: define required django version:
    install_requires=[
        'Django==2.2.24'
    ],
    dependency_links=[
        'https://pypi.python.org/simple/django/'
    ],
)
