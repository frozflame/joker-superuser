#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals

from volkanic.system import CommandRegistry

entries = {
    'joker.superuser.python.directory': 'pydir',
    'joker.superuser.python.entrypoint': 'pyent',
    'joker.superuser.shell.unsource': 'unsource',
    'joker.superuser.shell.cases': 'cases',
    'joker.superuser.dedup': 'dup',
    'joker.superuser.setop': 'setop',
}

registry = CommandRegistry(entries)

if __name__ == '__main__':
    registry()
