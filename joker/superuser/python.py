#!/usr/bin/env python3
# coding: utf-8

import os
from os.path import join


_nspkg = {
    'i': '__import__("pkg_resources").declare_namespace(__name__)',
    'p': '__path__ = __import__("pkgutil").extend_path(__path__, __name__)',
}


def _vk_join(d):
    return {k: join(v, k) for k, v in d}


class Project(object):
    _toplevel = [
        'setup.py',
        '.gitignore',
        'MANIFEST.in',
        'requirements.txt',
        'docs/',
    ]

    def __init__(self, nsp, pkg):
        """
        :param nsp: namespace
        :param pkg: package name
        """
        self.proj = '{}-{}'.format(nsp, pkg) if nsp else pkg
        self.nsp = nsp
        self.pkg = pkg
        self.common_dirs = {
            'docs': self.under_proj_dir('docs'),
            'templates': self.under_pkg_dir('templates'),
            'test': self.under_proj_dir(self.proj.replace('-', '_')),
        }
        self.common_files = _vk_join({
            '.gitignore': self.proj,
            'requirements.txt': self.proj,
            'MANIFEST.in': self.proj,
            'setup.py': self.proj,
            '__init__.py': self.under_pkg_dir(),
        })

    @classmethod
    def parse(cls, name):
        """
        :param name: e.g. "volkanic", "joker.superuser"
        :return: a Project instance
        """
        parts = name.split('.')
        if len(parts) == 1:
            return cls(parts[0], '')
        elif len(parts) == 2:
            return cls(parts[1], parts[1])
        else:
            raise ValueError

    def getlines_manifest(self):
        return [
            'include requirements.txt',
            'exclude test_jokersuperuser/*'
        ]

    def under_proj_dir(self, *paths):
        return join(self.proj, *paths)

    def under_pkg_dir(self, *paths):
        names = [self.proj, self.nsp, self.pkg]
        names = [s for s in names] + list(paths)
        return join(*names)

    def locate(self, name):
        if name.endswith('/'):
            return self.common_dirs.get(name[:-1])
        return self.common_files.get(name)

    def make_structure(self):
        for path in self.common_dirs.values():
            os.makedirs(path)
        for path in self.common_files.values():
            open(path, 'a').close()
