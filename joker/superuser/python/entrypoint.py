#!/usr/bin/env python3
# coding: utf-8

import os
import re

_template = r"""#!/usr/bin/env python3
# coding: utf-8
import re, sys; from {mod} import {call}
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit({call}())
"""

_regex = re.compile(r'(?P<cmd>\w+)=(?P<mod>\w[\w.]*\w):(?P<call>\w+)$')


def make_entrypoint_script(spec):
    spec = ''.join(spec.split())
    mat = _regex.match(spec)
    if not mat:
        raise ValueError('bad spec "{}"'.format(spec))
    print(_template.format(**mat.groupdict()))


class Spy(object):
    def __init__(self):
        self.args = None
        self.kwargs = None

    def __call__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def load_setup_file(self, path):
        import setuptools
        path = os.path.abspath(path)
        os.chdir(os.path.dirname(path))
        setuptools.setup = self
        code = open(path).read()
        exec(code, {'__file__': path})


def run(prog, args):
    spy = Spy()
    spy.load_setup_file(args[0])
    try:
        spec = spy.kwargs['entry_points']['console_scripts'][0]
    except LookupError:
        return
    make_entrypoint_script(spec)



