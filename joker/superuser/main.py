#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals


from volkanic.system import CommandRegistry

entries = {
    'joker.superuser.mkconf_apt': 'apt',
    'joker.superuser.misc.drawbox': 'box',
    'joker.superuser.misc.fontface': 'fontface',
    'joker.superuser.python.project': 'pkg',
    'joker.superuser.shell.associative': 'shell-assoc',
    'joker.superuser.shell.quote': 'shell-quote',
}

registry = CommandRegistry(entries)

if __name__ == '__main__':
    registry()
