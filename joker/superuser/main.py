#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals

from volkanic.system import CommandRegistry

entries = {
    'joker.superuser.pydir': 'pydir',
    'joker.superuser.pyentry': 'pyentry',
    'joker.superuser.unsource': 'unsource',
    'joker.superuser.cases': 'cases',
    'joker.superuser.dedup': 'dup',
    'joker.superuser.setop': 'setop',
    'joker.superuser.remove': 'rmdir',
    'joker.superuser.apt': 'apt',
}

registry = CommandRegistry(entries)

if __name__ == '__main__':
    registry()
