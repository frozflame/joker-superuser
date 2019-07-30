#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals

import platform
from volkanic.system import CommandRegistry

entries = {
    'joker.superuser.python.pkgdir': 'pkg',
    'joker.superuser.unix.abbrmap': 'abbrmap',
    'joker.superuser.unix.assoc': 'shell-assoc',
    'joker.superuser.unix.quote': 'shell-quote',
    'joker.superuser.misc.drawbox': 'box',
    'joker.superuser.misc.newline': 'nl',
    'joker.superuser.misc.fontface': 'fontface',
}

_macos_entries = {
    'joker.superuser.macos.share': 'share',
}


osname = platform.system().lower()

if osname == 'darwin':
    entries.update(_macos_entries)

# elif osname == 'windows':
#     handler = _windows_open
# else:
#     handler = _linux_open
# for path in paths:
#     handler(path)

registry = CommandRegistry(entries)

if __name__ == '__main__':
    registry()
