#!/usr/bin/env python3
# coding: utf-8

import os

from joker.textmanip.tabular import textfile_to_dict

from joker.superuser.utils import silent_function


@silent_function
def run(_, args):
    name = args[0]
    path = os.path.expanduser(args[1])
    d = textfile_to_dict(path)
    for k, v in d.items():
        if k.startswith('#'):
            continue
        v = os.path.expanduser(v)
        line = "{}[{}]='{}'".format(name, k, v)
        print(line, end=';')
