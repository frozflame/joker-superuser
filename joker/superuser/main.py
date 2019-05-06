#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals


from volkanic.system import CommandRegistry

entries = {
    'joker.superuser.mkconf_apt': 'apt',
    'joker.superuser.mkconf_network': 'iface',
}

registry = CommandRegistry(entries)

if __name__ == '__main__':
    registry()
