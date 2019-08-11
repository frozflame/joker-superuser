#!/usr/bin/env python3
# coding: utf-8

import os
import re
import sys
from os.path import isfile, abspath

from joker.textmanip.stream import ShellStream


def parse_fdupes_output(path):
    groups = [[]]
    with ShellStream.open(path) as stream:
        for line in stream.snl():
            if not line:
                groups.append([])
                continue
            if os.path.isfile(line):
                groups[-1].append(line)
    return groups


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


if __name__ == '__main__':
    parse_fdupes_output(sys.argv[1])
