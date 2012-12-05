#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='Jira Commando',
    version='1.0.0',
    description='A basic command line utility for listing, moving, and commenting on Jira issues.',
    long_description='',
    author='Josh Rooke-Ley',
    author_email='joshrl@me.com',
    url='https://github.com/joshrl/Jira-Commando',
    packages=find_packages(),
    install_requires=[
      'jira_python >=0.12',
      'keyring >= 0.10.1',
    ],
    entry_points={
        'console_scripts': [
            'jira = jiracommando.main:main',
        ]
    },
)
