#!/usr/bin/env python3
# coding: utf-8
import argparse
import os
import sys
import threading
import traceback
from collections import deque
from concurrent.futures import ThreadPoolExecutor

import requests
from joker.cast.syntax import printerr
from joker.minions.cache import CacheServer, ActiveTab


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
    val_cmtprefix = b'#'

    def __init__(self, sizelimit, path):
        super(AbbrmapServer, self).__init__()
        self.data = ActiveTab(sizelimit, path)
        self.cached_commands = {b'#request'}
        self.commands = {
            b'#xopen': self.cmd_xopen,
            b'#reload': self.cmd_reload,
            b'#update': self.cmd_update,
            b'#request': self.cmd_request,
            b'#version': self.cmd_version,
        }
        self._tpexec = ThreadPoolExecutor(max_workers=3)

    def lookup(self, key, val):
        if key in self.commands:
            return self._lookup_with_command(key, val)
        return super(AbbrmapServer, self).lookup(key, val)

    def _lookup_with_command(self, key, val):
        keyval = None
        if key in self.cached_commands:
            keyval = key + self.val_cmtprefix + val
            try:
                return self.data[keyval]
            except Exception:
                pass
        try:
            rv = self.commands[key](val)
        except Exception:
            traceback.print_exc()
            rv = self.val_none
        if key in self.cached_commands and rv:
            self.data[keyval] = rv
        return rv

    def _printdiff(self, vdata):
        udata = self.data.data
        keys = set(vdata)
        keys.update(udata)
        for k in keys:
            u = udata.get(k)
            v = vdata.get(k)
            if u != v:
                _printerr(k, u, v)

    @staticmethod
    def cmd_request(url):
        return requests.get(url).content

    @staticmethod
    def cmd_version(_):
        import joker.superuser
        return 'joker-superuser==' + joker.superuser.__version__

    def cmd_reload(self, _):
        self._tpexec.submit(self.data.reload)

    def cmd_update(self, _):
        self._tpexec.submit(self.data.update)

    def cmd_xopen(self, val):
        from volkanic.default import desktop_open
        val = b'.'.join(val.split())[:64]
        val = b'https://a.geekinv.com/s/api/' + val
        val = self.lookup(b'#request', val)
        desktop_open(val.decode('latin1'))
        return val

    def eviction(self, period=5):
        import time
        while True:
            time.sleep(period)
            self.data.evict()


def get_port_num():
    envvar = 'JOKER_SUPERUSER_ABBRMAP_PORT'
    try:
        return int(os.environ.get(envvar))
    except TypeError:
        return 8331


def run(prog, args):

    desc = 'abbrmap server'
    pr = argparse.ArgumentParser(prog=prog, description=desc)
    aa = pr.add_argument
    aa('-s', '--size', type=int, default=ActiveTab.default_sizelimit)
    aa('-t', '--tabfile', default='~/.joker/superuser/abbrmap.txt',
       help='path to a 2-column tabular text file')

    ns = pr.parse_args(args)
    try:
        svr = AbbrmapServer(ns.size, ns.tabfile)
    except Exception as e:
        printerr(e)
        sys.exit(1)
    threading.Thread(target=svr.eviction, daemon=True).start()
    svr.runserver('127.0.0.1', get_port_num())
