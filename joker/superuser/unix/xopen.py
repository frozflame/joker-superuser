#!/usr/bin/env python3
# coding: utf-8
import argparse
import os
import re

from volkanic.default import desktop_open


def get_port_num():
    envvar = 'JOKER_SUPERUSER_ABBRMAP_PORT'
    try:
        return int(os.environ.get(envvar))
    except TypeError:
        return 8331


def check_abbrmap():
    from joker.minions.utils import netcat
    try:
        resp = netcat('127.0.0.1', get_port_num(), b'#version')
    except Exception:
        return False
    return resp.startswith(b'joker-superuser')


def get_api_url(target):
    prefix = 'https://a.geekinv.com/s/api/'
    return prefix + '.'.join(target.split())[:64]


def _openurl(url):
    if not re.match(r'https?://', url):
        return
    try:
        desktop_open(url)
    except Exception as e:
        from joker.cast.syntax import printerr
        printerr(e)


def _aopen_query_webapi(qs):
    import requests
    api_url = get_api_url(qs)
    url = requests.get(api_url).text
    _openurl(url)


def _aopen_query_local(qs):
    from joker.minions.utils import netcat
    api_url = get_api_url(qs)
    line = ('#request ' + api_url).encode('latin1')
    url = netcat('127.0.0.1', get_port_num(), line).decode('latin1')
    _openurl(url)


def aopen(*targets):
    if not targets:
        return
    if check_abbrmap():
        func = _aopen_query_local
    else:
        func = _aopen_query_webapi
    if len(targets) == 1:
        return func(targets[0])
    from concurrent.futures import ThreadPoolExecutor
    pool = ThreadPoolExecutor(max_workers=4)
    return pool.map(func, targets)


def xopen(*targets):
    if not targets:
        return desktop_open('.')
    direct_locators = set()
    indirect_locators = set()
    exists = os.path.exists

    for t in targets:
        if exists(t) or re.match(r'(https?|file|ftp)://', t):
            direct_locators.add(t)
        elif re.match(r'[\w._-]{1,64}$', t):
            indirect_locators.add(t)
    desktop_open(*direct_locators)
    aopen(*indirect_locators)


def run(_, args):
    xopen(*args)


def run1(prog, args):
    desc = 'desktop open'
    pr = argparse.ArgumentParser(prog=prog, description=desc)
    aa = pr.add_argument
    aa('-a', action='store_true', help='query a.geekinv.com api')
    aa('target', nargs='+', help='path or url or query words')
    ns = pr.parse_args(args)
    if not ns.a:
        return desktop_open(*ns.target)
    if not check_abbrmap():
        return aopen(*ns.target)
    return xopen(*ns.target)
