#!/usr/bin/env python3
# coding: utf-8

import os
import re
import sys
from os.path import join, relpath
import logging

from joker.textmanip.tabular import format_help_section

from joker.superuser.utils import under_asset_dir
from joker.superuser.environ import GlobalInterface

_gi = GlobalInterface()
_logger = logging.Logger(__name__)


_nspinits = {
    'i': '__import__("pkg_resources").declare_namespace(__name__)',
    'p': '__path__ = __import__("pkgutil").extend_path(__path__, __name__)',
}


def _vk_join(d):
    return {k: join(v, k) for k, v in d.items()}


class ProjectDirectoryMaker(object):
    def __init__(self, nsp, pkg):
        """
        :param nsp: namespace
        :param pkg: package name
        """
        self.nsp = nsp.strip()
        self.pkg = pkg.strip()
        if self.nsp:
            names = [self.nsp, self.pkg]
        else:
            names = [self.pkg]
        self.names = names
        self.dot_name = '.'.join(names)
        self.hyf_name = '-'.join(names)
        self.uns_name = '_'.join(names)

        self.package_name = '.'.join(names)
        self.project_name = '-'.join(names)
        self.identifier = '_'.join(names)

        self.common_dirs = {
            'docs': self.under_proj_dir('docs'),
            'test': self.under_proj_dir('test_' + self.uns_name),
            'templates': self.under_pkg_dir('templates'),
        }
        self.common_files = _vk_join({
            '__init__.py': self.under_pkg_dir(),
            'requirements.txt': self.hyf_name,
            'MANIFEST.in': self.hyf_name,
            '.gitignore': self.hyf_name,
            'setup.py': self.hyf_name,
        })
        if self.nsp:
            p = join(self.hyf_name, self.nsp, '__init__.py')
            self.common_files['nspinit'] = p

    @classmethod
    def parse(cls, name):
        """
        :param name: e.g. "mypkg", "mynsp.mypkg"
        :return: a ProjectDirectoryMaker instance
        """
        mat = re.match(r'([_A-Za-z]\w*\.|)([_A-Za-z]\w*)', name)
        if not mat:
            raise ValueError('invalid pakcage name: ' + repr(name))
        return cls(mat.group(1)[:-1] or '', mat.group(2))

    def under_proj_dir(self, *paths):
        return join(self.hyf_name, *paths)

    def under_pkg_dir(self, *paths):
        parts = [self.hyf_name] + self.names + list(paths)
        return join(*parts)

    def locate(self, name):
        if name.endswith('/'):
            return self.common_dirs.get(name[:-1])
        return self.common_files.get(name)

    def make_dirs(self):
        for path in self.common_dirs.values():
            os.makedirs(path, exist_ok=True)
        for path in self.common_files.values():
            open(path, 'a').close()

    def sub(self, text):
        text = text.replace('__sus_hyf_name', self.hyf_name)
        text = text.replace('__sus_dot_name', self.dot_name)
        text = text.replace('__sus_uns_name', self.uns_name)
        text = text.replace('__sus_nsp', self.nsp)
        text = text.replace('__sus_pkg', self.pkg)
        return text

    def _gettext_setup(self, template_path):
        template_path = template_path or under_asset_dir('setup.txt')
        code = open(template_path).read()
        return self.sub(code)

    def gettext_setup(self, template_path=None):
        jinja2 = _gi.jinja2_env
        tpl = jinja2.get_template('setup.py.jinja2')
        return tpl.render(self.__dict__)

    def gettext_manifest(self):
        # CAUTION: not self.common_dirs['templates']!
        # relative to self.under_proj_dir()!
        return os.linesep.join([
            'include requirements.txt',
            'exclude {}/*'.format(
                relpath(self.common_dirs['test'], self.hyf_name),
            ),
            'recursive-include {} *.html'.format(
                relpath(self.common_dirs['templates'], self.hyf_name),
            )
        ]) + os.linesep

    def write(self, name, content):
        path = self.common_files.get(name)
        if path and content:
            with open(path, 'a') as fout:
                fout.write(content + os.linesep)

    def write_nspinit(self, approach):
        self.write('nspinit', _nspinits.get(approach))

    def write_version_variable(self):
        self.write('__init__.py', "__version__ = '0.0'")

    def write_requirements(self, lines):
        self.write('requirements.txt', os.linesep.join(lines))

    def write_setup(self, template_path=''):
        self.write('setup.py', self.gettext_setup(template_path))

    def write_manifest(self):
        self.write('MANIFEST.in', self.gettext_manifest())

    def write_gitignore(self, path=''):
        path = path or under_asset_dir('gitignore.txt')
        self.write('.gitignore', open(path).read())


def make_project(name, alt, setup, gitignore, require, nsp_approach):
    if alt == 'nspinit':
        print(_nspinits.get(nsp_approach, ''))
        return
    if alt == 'gitignore':
        print(open(under_asset_dir('gitignore.txt')).read())
        return

    mkr = ProjectDirectoryMaker.parse(name)
    if alt == 'sub':
        print(mkr.sub(sys.stdin.read()))
        return
    if alt == 'setup':
        print(mkr.gettext_setup(setup))
        return
    if alt == 'manifest':
        print(mkr.gettext_manifest())
        return

    try:
        # TODO
        return print(mkr.locate(alt or '') + '')
    except TypeError:
        pass

    if alt:
        raise ValueError('invalid action: ' + repr(alt))

    mkr.make_dirs()
    mkr.write_setup(setup)
    mkr.write_gitignore(gitignore)
    mkr.write_requirements(require or [])
    mkr.write_manifest()
    mkr.write_nspinit(nsp_approach)
    mkr.write_version_variable()


def run(prog=None, args=None):
    import argparse
    desc = 'Generate a python project structure'
    # s = ' (case sensitive)'
    epilog = '\n'.join([
        format_help_section('Namespace package approaches', _nspinits),
        'About namespace packages:',
        '  https://packaging.python.org/guides/packaging-namespace-packages/',
    ])
    parser = argparse.ArgumentParser(
        prog=prog, description=desc, epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    add = parser.add_argument

    add('-a', '--alt',
        choices=['nspinit', 'gitignore', 'sub', 'setup', 'manifest'],
        help='alternative action')

    add('-n', '--nsp-approach', choices=['i', 'p', 'e'],
        default='i', help='namespace package approach')

    add('-s', '--setup', metavar='template_setup.py',
        help='path to a custom setup.py template')

    add('-g', '--gitignore', metavar='template_gitignore.txt',
        help='path to a custom .gitignore template')

    add('-r', '--require', action='append', metavar='PACKAGE',
        help='example: -r six -r numpy>=1.0.0')

    add('name', metavar='[NAMESPACE.]PACKAGE_NAME[%QUERY]')
    ns = parser.parse_args(args)

    try:
        make_project(**vars(ns))
    except ValueError as e:
        print(str(e), file=sys.stderr)
