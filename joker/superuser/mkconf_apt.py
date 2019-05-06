#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals

import argparse
import datetime
import shutil
import subprocess
import sys

standard_path = '/etc/apt/sources.list'
description = "a script to generate " + standard_path

shortcuts = {
    'ustc': 'https://mirrors.ustc.edu.cn/ubuntu/',
    'tsinghua': 'https://mirrors.tuna.tsinghua.edu.cn/ubuntu/',
}

default = 'https://mirrors.tuna.tsinghua.edu.cn/ubuntu/'

template = """\
deb {0} {1} main restricted universe multiverse
deb {0} {1}-updates main restricted universe multiverse
deb {0} {1}-backports main restricted universe multiverse
deb {0} {1}-security main restricted universe multiverse
"""


def get_ubuntu_codename():
    return subprocess.check_output(['lsb_release', '-cs']).decode().strip()


def conf_format(url):
    url = shortcuts.get(url, url) or default
    codename = get_ubuntu_codename()
    return template.format(url, codename)


def conf_print(url):
    print(conf_format(url))


def backup_and_overwrite(content):
    now = datetime.datetime.now()
    path = now.strftime(standard_path + '.%y%m%d-%H%M%S')
    shutil.copyfile(standard_path, path)
    with open(standard_path, 'w') as fout:
        fout.write(content)


def conf_apply(url):
    try:
        backup_and_overwrite(conf_format(url))
    except PermissionError:
        print('You must be root to do this.')
        sys.exit(1)


def run(prog=None, args=None):
    parser = argparse.ArgumentParser(prog=prog, description=description)
    parser.add_argument(
        '-u', '--url',
        help='mirror url like "http://archive.ubuntu.com/ubuntu/"'
    )
    parser.add_argument(
        '-a', '--apply', action='store_true',
        help='apply to ' + standard_path,
    )
    ns = parser.parse_args(args)
    if ns.apply:
        conf_apply(ns.url)
    else:
        conf_print(ns.url)


if __name__ == '__main__':
    run()
