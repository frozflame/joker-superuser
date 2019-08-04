#!/usr/bin/env python3
# coding: utf-8
import argparse
import os

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


def aopen_nocache(*targets):
    import requests
    for t in targets:
        url = 'https://a.geekinv.com/s/api/' + '.'.join(t.split())[:64]
        try:
            desktop_open(requests.get(url).text)
        except Exception as e:
            from joker.cast.syntax import printerr
            printerr(e)


def aopen(*targets):
    from joker.minions.utils import netcat
    for t in targets:
        t = '.'.join(t.split())[:64]
        k = t.encode('utf-8')
        netcat('127.0.0.1', get_port_num(), b'#xopen ' + k)


def xopen(*targets):
    import re
    from os.path import exists
    direct_locators = set()
    indirect_locators = set()

    for t in targets:
        if exists(t) or re.match(r'(https?|file|ftp)://', t):
            direct_locators.add(t)
        elif re.match(r'[\w._-]{1,64}$', t):
            indirect_locators.add(t)
    desktop_open(*direct_locators)
    if check_abbrmap():
        return aopen(*indirect_locators)
    aopen_nocache(*indirect_locators)


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
