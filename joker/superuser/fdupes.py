#!/usr/bin/env python3
# coding: utf-8

import re
from os.path import isfile, abspath

from joker.cast.iterative import split
from joker.stream.shell import ShellStream


def parse_fdupes_output(path):
    with ShellStream.open(path).snl() as stream:
        for tup in split(stream, lambda x: not x):
            elements = tup[-1]
            if elements:
                yield elements


def check_existence(groups):
    for grp in groups:
        paths = [abspath(p) for p in grp if isfile(p)]
        if len(paths) > 1:
            yield paths


def search_pattern(groups, pattern):
    for grp in groups:
        for path in grp:
            if re.search(pattern, path):
                yield grp
                break


def _parse_args(prog, args):
    import argparse
    desc = 'search with regex in fdupes output'
    pr = argparse.ArgumentParser(prog=prog, description=desc)
    aa = pr.add_argument
    aa('-p', '--pattern', help='regular expression')
    aa('path', help='fdupes output text file')
    return pr.parse_args(args)


def run(prog, args):
    ns = _parse_args(prog, args)
    groups = parse_fdupes_output(ns.path)
    groups = check_existence(groups)
    if ns.pattern:
        groups = search_pattern(groups, ns.pattern)
    for grp in groups:
        for line in grp:
            print(line)
        print()
