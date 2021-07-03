#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals

import volkanic

cmddef = """
pydir       joker.superuser.tools.pydir
pyentry     joker.superuser.tools.pyentry
unsource    joker.superuser.unsource
cases       joker.superuser.cases
dup         joker.superuser.dedup
setop       joker.superuser.setop
rmdir       joker.superuser.remove
apt         joker.superuser.tools.apt
url         joker.superuser.tools.urls
urls        joker.superuser.tools.urls:runloop
"""

_prog = 'python3 -m joker.superuser'
registry = volkanic.CommandRegistry.from_cmddef(cmddef, _prog)

if __name__ == '__main__':
    registry()
