#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals

import argparse


def newline_conv(path, nl, suffix):
    with open(path) as fin, open(path + suffix, 'w', newline=nl) as fout:
        for line in fin:
            fout.write(line)


def run(prog, args):
    desc = 'Convert newlines'
    parser = argparse.ArgumentParser(prog=prog, description=desc)
    parser.add_argument('-s', '--style', choices=['n', 'rn', 'r'])
    parser.add_argument('path', help='an input data file')
    args = parser.parse_args(args)
    nls = {'n': '\n', 'rn': '\r\n', 'r': '\r'}
    suffix = '.{}.txt'.format(args.style)
    newline_conv(args.path, nls.get(args.style), suffix)
