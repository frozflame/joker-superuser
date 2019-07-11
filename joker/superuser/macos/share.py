#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals

import os
import subprocess
import sys


def share_a_dir(path):
    if not os.path.isdir(path):
        raise ValueError('not a dir: {}'.format(path))
    name = os.path.split(path)[1]
    real = os.path.realpath(path)
    cmd = ['sharing', '-a', real, '-s', '001', '-S', name, '-n', name]
    print(' '.join(cmd))
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        pass


def run(_, args):
    if os.getuid() != 0:
        sys.exit('only root can do this')

    for path in args:
        try:
            share_a_dir(path)
        except subprocess.CalledProcessError:
            sys.exit(1)
