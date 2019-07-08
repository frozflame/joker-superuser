#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals

import argparse


def make_title_box(title, comment='#', width=50):
    """
    # +--------------------------------------------------+
    # |                                                  |
    # |                  Title is here                   |
    # |                                                  |
    # +--------------------------------------------------+
    """
    lines = list()
    lines.append('+{}+'.format('-' * width))
    lines.append('|{}|'.format(' ' * width))
    lines.append('|{}|'.format(title.center(width)))
    lines.append('|{}|'.format(' ' * width))
    lines.append('+{}+'.format('-' * width))
    return ['{} {}'.format(comment, l) for l in lines]


def run(prog=None, args=None):
    desc = 'Draw title box'
    pr = argparse.ArgumentParser(prog=prog, description=desc)
    pr.add_argument('-t', '--title', default="Welcome",
                    help='text in the box')
    pr.add_argument('-c', '--comment', default='#',
                    help='comment symbol, e.g. # or //')
    pr.add_argument('-w', '--width', type=int, default=50,
                    help='width of the box')
    ns = pr.parse_args(args)
    for line in make_title_box(ns.title, ns.comment, ns.width):
        print(line)
