#!/usr/bin/env python3
# coding: utf-8
import argparse
import sys
import threading
import time
from collections import deque
from os.path import getmtime, expanduser, isfile

from joker.cast.syntax import printerr
from joker.minions.cache import CacheServer
from joker.textmanip.stream import nonblank_lines_of


def _printerr(*args, **kwargs):
    parts = []
    for a in args:
        if isinstance(a, bytes):
            parts.append(a.decode())
        elif isinstance(a, (deque, list, tuple)):
            parts.extend(a)
    kwargs.setdefault('sep', ':')
    printerr(*parts, **kwargs)


class AbbrmapServer(CacheServer):
    def __init__(self, tabfile):
        super(AbbrmapServer, self).__init__()
        self.tabfile = expanduser(tabfile)
        self.data = self._load_tabfile()

    def _getmtime(self):
        return int(getmtime(self.tabfile) * 1000)

    def _conditional_sleep(self, duration, chkkey):
        t = .2
        n = int(duration / t)
        for _ in range(n):
            if self.data.pop(chkkey, None):
                break
            time.sleep(t)

    def _load_tabfile(self):
        data = {}
        for line in nonblank_lines_of(self.tabfile, 'rb'):
            if line.startswith(b'#'):
                continue
            parts = line.split(maxsplit=1)
            if len(parts) != 2:
                continue
            k, v = parts
            v = expanduser(v)
            data[k] = v
        return data

    def _printdiff(self, data, mtimes):
        keys = set(data)
        keys.update(self.data)
        for k in keys:
            u = self.data.get(k)
            v = data.get(k)
            if u != v:
                _printerr(mtimes, k, u, v)

    def watch(self):
        mtimes = deque([0], 2)
        self.data[b'#'] = b'.'
        while True:
            # only check mtime every 2 minutes unless b'#' found
            self._conditional_sleep(120, b'#')
            mtimes.append(self._getmtime())
            if mtimes[0] == mtimes[1]:
                _printerr(mtimes, 'Same')
                continue
            _printerr(mtimes, 'Modified')
            data = self._load_tabfile()
            self._printdiff(data, mtimes)
            self.data = data


def run(prog, args):
    desc = 'abbrmap server'
    pr = argparse.ArgumentParser(prog=prog, description=desc)
    pr.add_argument('-p', '--port', type=int, default=8331)
    pr.add_argument('-t', '--tabfile',
                    default='~/.joker/superuser/abbrmap.txt',
                    help='path to a 2-column tabular text file')

    ns = pr.parse_args(args)
    try:
        svr = AbbrmapServer(ns.tabfile)
    except Exception as e:
        printerr(e)
        sys.exit(1)

    threading.Thread(target=svr.watch).start()
    svr.runserver('127.0.0.1', ns.port)
