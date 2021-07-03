#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals

from volkanic.system import CommandRegistry


cmddef = """
pydir       joker.superuser.pydir
pyentry     joker.superuser.pyentry
unsource    joker.superuser.unsource
cases       joker.superuser.cases
dup         joker.superuser.dedup
setop       joker.superuser.setop
rmdir       joker.superuser.remove
apt         joker.superuser.tools.apt
url         joker.superuser.tools.urls
urls        joker.superuser.tools.urls:runloop
"""

registry = CommandRegistry.from_cmddef(cmddef)

if __name__ == '__main__':
    registry()
