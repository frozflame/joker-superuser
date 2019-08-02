#!/usr/bin/env python3
# coding: utf-8

import argparse
import os.path as osp
import re
import shlex
import sys
import weakref
from collections import deque


# TODO
class CircularReferenceDetector(object):
    def __init__(self):
        self._data = {}

    def add(self, referer, referee):
        self._data.setdefault(referee, referer)


class CircularReferenceError(IOError):
    pass


def _abspath(path):
    return osp.abspath(osp.expanduser(path))


class VirtualFile(object):
    __slots__ = ['remote', 'locator', '_file']
    opened_files = weakref.WeakSet()

    def __init__(self, locator):
        self._file = None
        self.remote = bool(re.match(r'https?://', locator))
        self.locator = locator if self.remote else _abspath(locator)

    def __bool__(self):
        return self.remote or osp.isfile(self.locator)

    def __iter__(self):
        if self._file is None:
            self._file = self._open()
        return self._file

    def _open(self):
        if self.remote:
            import io
            import requests
            return io.StringIO(requests.get(self.locator).text)
        else:
            fin = open(self.locator)
            self.opened_files.add(fin)
            return fin

    @classmethod
    def close_all(cls):
        for f in cls.opened_files:
            try:
                f.close()
            except Exception:
                pass


def check_for_source(line):
    line = line.strip()
    parts = shlex.split(line, comments=True)
    if len(parts) == 2 and parts[0] in ['.', 'source']:
        return VirtualFile(parts[1])


def source_expand(locators, fout):
    vfs = [VirtualFile(loc) for loc in locators]
    stack = deque(reversed(vfs))
    visited = set()
    while stack:
        vf = stack.pop()
        visited.add(vf.locator)
        for line in vf:
            new_vf = check_for_source(line)
            if not new_vf:
                fout.write(line)
                continue
            if new_vf.locator in visited:
                msg = '{}=>{}'.format(vf.locator, new_vf.locator)
                raise CircularReferenceError(msg)
            stack.extend([vf, new_vf])
            break


def _rc(name):
    from joker.superuser import utils
    utils.make_joker_superuser_dir()
    return utils.under_joker_superuser_dir(name)


def _dotrc(name):
    return _abspath('~/.' + name)


def never_sourced(locator, target):
    target_vf = VirtualFile(target)
    for line in VirtualFile(locator):
        new_vf = check_for_source(line)
        if new_vf and new_vf.locator == target_vf.locator:
            return
    return target_vf


def add_source(path, target):
    target_vf = never_sourced(path, target)
    if not target_vf:
        return
    with open(path, 'a') as fout:
        line = '\nsource ' + shlex.quote(target_vf.locator) + '\n'
        fout.write(line)


def apply(name):
    assert name in ['zshrc', 'bashrc']


def _run(locators, outpath):
    if not outpath or outpath == '-':
        fout = sys.stdout
    else:
        fout = open(outpath, 'w')
        VirtualFile.opened_files.add(fout)
    try:
        source_expand(locators, fout)
    except Exception as e:
        from joker.cast.syntax import printerr
        VirtualFile.close_all()
        printerr(e)


def run(prog, args):
    desc = 'concatenate shell scripts with sourced files replaced by contents'
    pr = argparse.ArgumentParser(prog=prog, description=desc)
    pr.add_argument('-a', '--apply', choices=['zshrc', 'bashrc'])
    pr.add_argument('files', nargs='+', help='shell scripts')
    ns = pr.parse_args(args)
    if not ns.apply:
        return _run(ns.files, '-')
    outpath = _rc(ns.apply)
    _run(ns.files, outpath)
    add_source(_dotrc(ns.apply), outpath)
