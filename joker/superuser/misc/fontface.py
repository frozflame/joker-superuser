#!/usr/bin/env python3
# coding: utf-8
import subprocess
import os
import shlex
import pathlib

_css_tmpl = """
@font-face {
    font-family: "{0}";
    src: url("/static/fonts/{0}.eot");    /* IE9 Compat Modes */
    src: local("Noto Serif CJK SC Medium"),
    url("/static/fonts/{0}.eot?#iefix") format("embedded-opentype"),    /* IE6-IE8 */
    url("/static/fonts/{0}.otf") format("opentype"),    /* Open Type Font */
    url("/static/fonts/{0}.svg#{0}") format("svg"),     /* Legacy iOS */
    url("/static/fonts/{0}.ttf") format("truetype"),    /* Safari, Android, iOS */
    url("/static/fonts/{0}.woff") format("woff"),       /* Modern Browsers */
    url("/static/fonts/{0}.woff2") format("woff2");     /* Modern Browsers */
    font-weight: normal;
    font-style: normal;
}
"""

_script_tmpl = r"""
#!fontforge
Open($1)
Generate($1:r + ".svg")
Generate($1:r + ".eot")
Generate($1:r + ".ttf")
Generate($1:r + ".woff")
Generate($1:r + ".woff2")
"""


class FontFaceMaker(object):
    def __init__(self, path):
        self.px = pathlib.Path(path).absolute()

    def format_css(self):
        return _css_tmpl.replace('{0}', self.px.stem)

    def format_fontforge_script(self):
        px = self.px
        lines = _script_tmpl.strip().splitlines()
        lines = [l for l in lines if px.suffix not in l]
        lines[0] = lines[0].format(shlex.quote(str(px)))
        return os.linesep.join(lines)


def run(_, args):
    ffm = FontFaceMaker(args[0])
    px_out = ffm.px.with_name('_fontface.' + ffm.px.name)
    with open(px_out.with_suffix('.css'), 'w') as fout:
        fout.write(ffm.format_css())
    px_script = px_out.with_suffix('.pe')
    with open(px_script, 'w') as fout:
        fout.write(ffm.format_fontforge_script())
    cmd = ['fontforge', '-script', str(px_script), str(ffm.px)]
    print(*[shlex.quote(s) for s in cmd])
    subprocess.run(cmd)
