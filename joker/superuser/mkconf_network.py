#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals

import argparse
import os
import random
import socket
import sys

standard_path = '/etc/network/interfaces'
description = "a helper script for editing " + standard_path

template = """
#auto {0}
#iface {0} inet static
#    address 192.168.2.{1}
#    netmask 255.255.255.0
#    network 192.168.2.0
#    broadcast 192.168.2.255
#    gateway 192.168.2.1
#    dns-nameservers 64.6.64.6 195.46.39.39
"""


def list_interfaces():
    names = os.listdir('/sys/class/net')
    return [x for x in names if x.startswith('e') or x.startswith('w')]


def get_machine_number():
    hostname = socket.gethostname()
    if hostname.startswith('MR'):
        return int(hostname.replace('MR', ''))
    return random.randint(200, 250)


def ifconf_append(content):
    with open(standard_path, 'a') as fout:
        fout.write('\n')
        fout.write(content)


def conf_format():
    sections = []
    num = get_machine_number()
    for ifn in list_interfaces():
        sections.append(template.format(ifn, num))
    return '\n'.join(sections)


def conf_print():
    print(conf_format())


def conf_apply():
    try:
        ifconf_append(conf_format())
    except PermissionError:
        print('You must be root to do this.')
        sys.exit(1)


def run(prog=None, args=None):
    parser = argparse.ArgumentParser(prog=prog, description=description)
    parser.add_argument(
        '-a', '--apply', action='store_true',
        help='apply to ' + standard_path,
    )
    ns = parser.parse_args(args)
    if ns.apply:
        conf_apply()
    else:
        conf_print()


if __name__ == '__main__':
    run()
