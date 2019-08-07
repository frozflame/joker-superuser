#!/usr/bin/env python3
# coding: utf-8

import argparse
import re
import shlex

from joker.textmanip.stream import nonblank_lines_of


def run(prog=None, args=None):
    desc = 'Quote each line of text'
    pr = argparse.ArgumentParser(prog=prog, description=desc)
    aa = pr.add_argument
    aa('-f', '--formula', default='QUOTED', help='e.g. -f "rm -fr QUOTED"')
    aa('path', metavar='PATH', help='use - to read from STDIN')
    ns = pr.parse_args(args)
    regex = re.compile(r'\bQUOTED\b')
    for line in nonblank_lines_of(ns.path):
        quoted = shlex.quote(line)
        line = regex.sub(quoted, ns.formula)
        print(line)
