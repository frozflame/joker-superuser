#!/usr/bin/env python3
# coding: utf-8

import os
import re
import sys
from os.path import join

from joker.superuser.utils import under_templates_dir

_nspinit_approaches = {
    'i': '__import__("pkg_resources").declare_namespace(__name__)',
    'p': '__path__ = __import__("pkgutil").extend_path(__path__, __name__)',
}


def _vk_join(d):
    return {k: join(v, k) for k, v in d.items()}


class ProjectDirMaker(object):
    def __init__(self, nsp, pkg):
        """
        :param nsp: namespace
        :param pkg: package name
        """
        nsp = nsp.strip()
        pkg = pkg.strip()
        self.proj = '{}-{}'.format(nsp, pkg) if nsp else pkg
        self.nsp = nsp
        self.pkg = pkg
        names = [self.proj, self.nsp, self.pkg]
        names = [s for s in names if s]
        self.names = names
        testdir_name = '_'.join(['test'] + self.names[1:])
        self.common_dirs = {
            'docs': self.under_proj_dir('docs'),
            'templates': self.under_pkg_dir('templates'),
            'test': self.under_proj_dir(testdir_name),
        }
        self.common_files = _vk_join({
            '.gitignore': self.proj,
            'requirements.txt': self.proj,
            'MANIFEST.in': self.proj,
            'setup.py': self.proj,
            '__init__.py': self.under_pkg_dir(),
        })
        if self.nsp:
            self.common_files['nspinit'] = self.under_proj_dir('__init__.py')

    @classmethod
    def parse(cls, name):
        """
        :param name: e.g. "volkanic", "joker.superuser"
        :return: a ProjectDirMaker instance
        """
        mat = re.match(r'([_A-Za-z]\w+\.)?([_A-Za-z]\w+)', name)
        if not mat:
            raise ValueError('invalid pakcage name: ' + repr(name))
        return cls(mat.group(1)[:-1] or '', mat.group(2))

    def under_proj_dir(self, *paths):
        return join(self.proj, *paths)

    def under_pkg_dir(self, *paths):
        return join(*(self.names + list(paths)))

    def locate(self, name):
        if name.endswith('/'):
            return self.common_dirs.get(name[:-1])
        return self.common_files.get(name)

    def make_dirs(self):
        for path in self.common_dirs.values():
            os.makedirs(path)
        for path in self.common_files.values():
            open(path, 'a').close()

    def sub(self, text):
        text = text.replace('__sus_h_name', self.proj)
        text = text.replace('__sus_i_name', '.'.join(self.names[1:]))
        text = text.replace('__sus_u_name', '_'.join(self.names[1:]))
        text = text.replace('__sus_namespace', self.nsp)
        text = text.replace('__sus_package', self.pkg)
        return text

    def gettext_setup(self, template_path):
        template_path = template_path or under_templates_dir('setup.txt')
        code = open(template_path).read()
        return self.sub(code)

    def gettext_manifest(self):
        templates_path = os.path.sep.join(self.names[1:] + ['templates'])
        return os.linesep.join([
            'include requirements.txt',
            'exclude {}/*'.format(self.common_dirs['test']),
            'recursive-include {} *.html'.format(templates_path)
        ]) + os.linesep

    def write(self, name, content):
        path = self.common_files.get(name)
        if path and content:
            with open(path, 'w') as fout:
                fout.write(content + os.linesep)

    def write_nspinit(self, approach):
        self.write('nspinit', _nspinit_approaches.get(approach))

    def write_version_variable(self):
        self.write('__init__.py', "__version__ = '0.0'")

    def write_requirements(self, lines):
        self.write('requirements.txt', os.linesep.join(lines))

    def write_setup(self, template_path=''):
        self.write('setup.py', self.gettext_setup(template_path))

    def write_manifest(self):
        self.write('MANIFEST.in', self.gettext_manifest())

    def write_gitignore(self, path=''):
        path = path or under_templates_dir('gitignore.txt')
        self.write('.gitignore', open(path).read())


def make_project(name, setup, gitignore, require, nspinit_approach):
    name, query = (name.split('%', maxsplit=1) + [''])[:2]
    if query == 'nspinit':
        print(_nspinit_approaches.get(nspinit_approach, ''))
        return
    if query == 'gitignore':
        print(open(under_templates_dir('gitignore.txt')).read())
        return

    mkr = ProjectDirMaker.parse(name)
    if query == 'sub':
        print(mkr.sub(sys.stdin.read()))
        return
    if query == 'setup':
        print(mkr.gettext_setup(setup))
        return
    if query == 'manifest':
        print(mkr.gettext_manifest())
        return

    try:
        return print(mkr.locate(query) + '')
    except TypeError:
        pass

    if query:
        raise ValueError('invalid query: ' + repr(query))

    mkr.make_dirs()
    mkr.write_setup(setup)
    mkr.write_gitignore(gitignore)
    mkr.write_requirements(require)
    mkr.write_manifest()
    mkr.write_nspinit(nspinit_approach)
    mkr.write_version_variable()


def run(prog=None, args=None):
    import argparse
    desc = 'generate a python project structure'
    s = ' (case sensitive)'
    # epilog = '\n'.join([
    #     format_help_section('Variables' + s, _variables),
    #     format_help_section('Safe presets', _safe_presets),
    #     format_help_section('Risky presets', _risky_presets),
    # ])
    pr = argparse.ArgumentParser(
        prog=prog, description=desc,  # epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    pr.add_argument('-n', '--nspinit-approach', choices=['i', 'p', 'e'],
                    default='i', help='namespace package style')
    pr.add_argument('-s', '--setup', metavar='template_setup.py',
                    help='template for setup.py')
    pr.add_argument('-g', '--gitignore', metavar='template_gitignore.txt',
                    help='template for .gitignore')
    pr.add_argument('-r', '--require', action='append',
                    metavar='PKG', help='example: -r six -r numpy>=1.0.0')
    pr.add_argument('name')
    ns = pr.parse_args(args)
    try:
        make_project(**vars(ns))
    except ValueError as e:
        print(str(e), file=sys.stderr)
