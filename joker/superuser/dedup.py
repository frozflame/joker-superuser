#!/usr/bin/env python3
# coding: utf-8

import os
import re
import sys
from collections import defaultdict

from joker.cast.iterative import split
from joker.stream.shell import ShellStream
from joker.stream.utils import checksum

from joker.superuser import utils


# TODO: use a sha1sum txt file


def _thresh(size, minsize):
    if size >= minsize:
        return size


def get_sizefunc(minsize):
    sizefunc = utils.silent_function(os.path.getsize)
    if not minsize:
        return sizefunc
    return lambda p: _thresh(sizefunc(p), minsize)


@utils.silent_function
def chksum(path):
    return checksum(path).digest()


@utils.silent_function
def chksum_head(path, length=1024):
    return checksum(path, length=length).digest()


def _plural(grp):
    if len(grp) > 1:
        return grp


def _subgroup(groups, kfunc, gfunc):
    """
    separate each group into sub-groups
    :param groups: a list of lists
    :param kfunc: kfunc(path) => a differentiating property of a file,
        or None to ignore that file
    :param gfunc: gfunc(group) => a modified group,
        or None to ignore that group
    :return: a list of lists (sub-groups)
    """
    subgrps = []
    for grp in groups:
        aux = defaultdict(list)
        for path in grp:
            k = kfunc(path)
            if k is not None:
                aux[k].append(path)
        batch = (gfunc(g) for g in aux.values())
        batch = (g for g in batch if g is not None)
        subgrps.extend(batch)
    return subgrps


def find_duplicates(dirs, minsize=0, bold=False):
    all_files = []
    for path in dirs:
        all_files.extend(utils.find_regular_files(path))
    sizefunc = get_sizefunc(minsize)
    grps = _subgroup([all_files], sizefunc, _plural)
    grps = _subgroup(grps, chksum_head, _plural)
    if not bold:
        grps = _subgroup(grps, chksum, _plural)
    for grp in grps:
        grp.sort()
    return grps


def parse_fdupes_output(path):
    with ShellStream.open(path).snl() as stream:
        for tup in split(stream, lambda x: not x):
            elements = tup[-1]
            if elements:
                yield elements


def check_existence(groups):
    for grp in groups:
        paths = [p for p in grp if os.path.isfile(p)]
        if len(paths) > 1:
            paths.sort(reverse=True)
            yield paths


def search_pattern(groups, pattern):
    for grp in groups:
        for path in grp:
            if re.search(pattern, path):
                yield grp
                break


def _make_pairs(paths, protect_regex):
    pairs = []
    for i, path in enumerate(paths):
        if protect_regex.match(path):
            pairs.append((0, path))
        else:
            pairs.append((1 + i, path))
    pairs.sort()
    return pairs


def prioritize(groups, protect=None):
    if protect:
        regex = re.compile(protect)
        for grp in groups:
            yield _make_pairs(grp, regex)
    else:
        for grp in groups:
            yield [(1 + i, p) for i, p in enumerate(grp)]


def _make_script(pairs):
    from shlex import quote
    pairs = list(pairs)
    if not any(p[0] for p in pairs):
        return
    path = pairs[0][1]
    print('#', quote(path))
    for prio, path in pairs[1:]:
        if prio:
            print('rm -f', quote(path))
        else:
            print('#', quote(path))
    print()


def _parse_args(prog, args):
    import argparse
    desc = 'find duplicating files recursively'
    pr = argparse.ArgumentParser(prog=prog, description=desc)
    aa = pr.add_argument

    aa('-B', '--bold', action='store_true',
       help='skip full-size checksum comparison')

    aa('-s', '--size', type=int, default=1,
       help='minimum size for consideration')

    aa('-p', '--pattern', metavar='regex',
       help='select a subset of duplicating groups')

    aa('-P', '--protect', metavar='regex',
       help='prevent certain file from being deleted')

    aa('-f', '--fdupes', help='an fdupes output file')
    aa('dirs', metavar='DIR', nargs='*', help='target directory')
    return pr.parse_args(args)


def run(prog, args):
    ns = _parse_args(prog, args)
    if ns.fdupes:
        if ns.dirs:
            print('conflicting arguments: -f/--fdupes and dirs', file=sys.stderr)
        groups = parse_fdupes_output(ns.path)
        groups = check_existence(groups)
    else:
        groups = find_duplicates(ns.dirs, minsize=ns.size, bold=ns.bold)
    if ns.pattern:
        groups = search_pattern(groups, ns.pattern)
    p_groups = prioritize(groups, ns.protect)
    for pgrp in p_groups:
        _make_script(pgrp)
