#!/usr/bin/env python3
# coding: utf-8

import os
import re

import setuptools
from setuptools import find_namespace_packages

# CAUTION:
# Do NOT import your package from your setup.py

namespace = 'joker'
package_name = 'superuser'
description = 'tools for power users'


def read(filename):
    with open(filename) as f:
        return f.read()


def _find_version():
    if namespace:
        path = '{}/{}/__init__.py'.format(namespace, package_name)
    else:
        path = '{}/__init__.py'.format(package_name)
    root = os.path.dirname(__file__)
    path = os.path.join(root, path)
    regex = re.compile(
        r'''^__version__\s*=\s*('|"|'{3}|"{3})([.\w]+)\1\s*(#|$)''')
    with open(path) as fin:
        for line in fin:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            mat = regex.match(line)
            if mat:
                return mat.groups()[1]
    raise ValueError('__version__ definition not found')


config = {
    'name': 'joker-superuser',
    'version': _find_version(),
    'description': '' + description,
    'keywords': 'sysadmin',
    'url': 'https://github.com/frozflame/joker-superuser',
    'author': 'frozflame',
    'author_email': 'frozflame@outlook.com',
    'license': "GNU General Public License (GPL)",
    'packages': find_namespace_packages(include=['joker.*']),
    'zip_safe': False,
    'install_requires': read("requirements.txt"),
    'entry_points': {
        'console_scripts': ['sus = joker.superuser.__main__:registry'],
    },
    'classifiers': [
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    # ensure copy static file to runtime directory
    'include_package_data': True,
    'long_description': read('README.md'),
    'long_description_content_type': "text/markdown",
}

if namespace:
    config['name'] = '{}-{}'.format(namespace, package_name)
    config['namespace_packages'] = [namespace]

setuptools.setup(**config)
