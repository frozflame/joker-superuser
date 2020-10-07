#!/usr/bin/env python3
# coding: utf-8

from __future__ import print_function, unicode_literals

import re
import os
import sys
from glob import glob

sysname = os.uname().sysname


def _printerr(*args):
    print(*args, file=sys.stderr)


def write_file(text, *paths):
    for path in paths:
        with open(path, 'w') as fout:
            fout.write(text)


def write_gimp_menurc():
    if sysname == 'Darwin':
        prefix = '~/Library/Application Support/GIMP/2.*'
    else:
        return
    prefix = os.path.expanduser(prefix)
    paths = [os.path.join(p, 'menurc') for p in glob(prefix)]
    write_file(text_menurc, *paths)


def rewrite_info_plist():
    if sysname != 'Darwin':
        return _printerr('This tweak is macos-only.')
    pattern = '/Applications/GIMP*.app/Contents/Info.plist'
    paths = glob(pattern)
    if not len(paths) == 1:
        return _printerr('Found multiple GIMP*.app installed')
    path = paths[0]
    text = open(path).read()
    new_text = re.sub(
        r'(<key>CFBundleName</key>[\s\r\n]+<string>GIMP)[-.\d]+(</string>)',
        r'\1\2', text,
    )
    if new_text == text:
        return _printerr('Not changed:', path)
    with open(path, 'w') as fout:
        fout.write(new_text)


def rename_app_dir():
    if sysname != 'Darwin':
        return _printerr('This tweak is macos-only.')
    pattern = '/Applications/GIMP*.app'
    paths = glob(pattern)
    if not len(paths) == 1:
        return _printerr('Found multiple GIMP*.app installed')
    path = paths[0]
    new_path = '/Applications/GIMP.app'
    if path == new_path:
        return _printerr('Alread the good name:', new_path)
    os.rename(path, new_path)


text_menurc = r"""\
; gimp GtkAccelMap rc-file         -*- scheme -*-
; macOS: ~/Library/Application Support/GIMP/2.10
; Windows: C:\Users\<YourName>\AppData\Roaming\GIMP\2.10
; GNU/Linux: ~/.config/GIMP/2.10
; GNU/Linux (using Flatpak package): ~/.var/app/org.gimp.GIMP/config/GIMP/2.10
; GNU/Linux (using Snap package): ~/snap/gimp/current/.config/GIMP/2.10

(gtk_accel_path "<Actions>/view/view-shrink-wrap" "")
(gtk_accel_path "<Actions>/plug-in/plug_in_iwarp" "<Primary><Shift>x")
(gtk_accel_path "<Actions>/layers/layers-duplicate" "<Primary>j")
(gtk_accel_path "<Actions>/plug-in/plug_in_c_astretch" "<Primary><Shift><Alt>l")
(gtk_accel_path "<Actions>/context/context-brush-select-next" "period")
(gtk_accel_path "<Actions>/view/view-show-grid" "<Primary><Alt>apostrophe")
(gtk_accel_path "<Actions>/tools/tools-color-balance" "<Primary>b")
(gtk_accel_path "<Actions>/tools/tools-rotate" "")
(gtk_accel_path "<Actions>/image/image-rotate-270" "7")
(gtk_accel_path "<Actions>/layers/layers-mode-next" "plus")
(gtk_accel_path "<Actions>/dialogs/dialogs-brushes" "")
(gtk_accel_path "<Actions>/tools/tools-by-color-select" "<Primary><Shift>c")
(gtk_accel_path "<Actions>/tools/tools-vector" "p")
(gtk_accel_path "<Actions>/dialogs/dialogs-tool-options" "F5")
(gtk_accel_path "<Actions>/dialogs/dialogs-channels" "<Shift>F7")
(gtk_accel_path "<Actions>/qmask/qmask-toggle" "q")
(gtk_accel_path "<Actions>/tools/tools-value-2-increase" "")
(gtk_accel_path "<Actions>/layers/layers-alpha-selection-replace" "<Alt>a")
(gtk_accel_path "<Actions>/file/file-open-recent-10" "")
(gtk_accel_path "<Actions>/plug-in/plug_in_colortoalpha" "<Primary><Shift>a")
(gtk_accel_path "<Actions>/select/select-feather" "<Primary><Shift>d")
(gtk_accel_path "<Actions>/tools/tools-align" "")
(gtk_accel_path "<Actions>/layers/layers-select-top" "<Alt>braceright")
(gtk_accel_path "<Actions>/select/select-float" "")
(gtk_accel_path "<Actions>/tools/tools-desaturate" "<Primary><Shift>u")
(gtk_accel_path "<Actions>/select/select-invert" "<Primary><Shift>i")
(gtk_accel_path "<Actions>/plug-in/tiny_fu_refresh" "<Primary><Shift><Alt>t")
(gtk_accel_path "<Actions>/layers/layers-lower-to-bottom" "<Primary>braceleft")
(gtk_accel_path "<Actions>/layers/layers-lower" "<Primary>bracketleft")
(gtk_accel_path "<Actions>/image/image-convert-indexed" "backslash")
(gtk_accel_path "<Actions>/view/view-zoom-1-1" "<Primary><Alt>0")
(gtk_accel_path "<Actions>/view/view-scroll-page-left" "<Primary>Page_Up")
(gtk_accel_path "<Actions>/view/view-zoom-fit-to" "<Primary>0")
(gtk_accel_path "<Actions>/dialogs/dialogs-undo-history" "<Shift>F9")
(gtk_accel_path "<Actions>/layers/layers-resize-to-image" "<Alt>y")
(gtk_accel_path "<Actions>/plug-in/plug_in_gauss" "<Primary><Shift>b")
(gtk_accel_path "<Actions>/tools/tools-curves" "<Primary>m")
(gtk_accel_path "<Actions>/plug-in/plug_in_bump_map" "<Primary><Shift>m")
(gtk_accel_path "<Actions>/tools/tools-airbrush" "j")
(gtk_accel_path "<Actions>/image/image-flatten" "<Shift>i")
(gtk_accel_path "<Actions>/image/image-merge-layers" "<Primary><Shift>e")
(gtk_accel_path "<Actions>/view/view-scroll-page-right" "<Primary>Page_Down")
(gtk_accel_path "<Actions>/view/view-snap-to-guides" "<Primary>semicolon")
(gtk_accel_path "<Actions>/drawable/drawable-invert" "<Primary>i")
(gtk_accel_path "<Actions>/tools/tools-paint-brush-size-increase" "bracketright")
(gtk_accel_path "<Actions>/file/file-revert" "F12")
(gtk_accel_path "<Actions>/plug-in/plug-in-iwarp" "<Primary><Shift>x")
(gtk_accel_path "<Actions>/context/context-brush-select-previous" "comma")
(gtk_accel_path "<Actions>/tools/tools-convolve" "r")
(gtk_accel_path "<Actions>/file/file-export-to" "")
(gtk_accel_path "<Actions>/tools/tools-magnify" "z")
(gtk_accel_path "<Actions>/view/view-zoom-in" "<Primary>equal")
(gtk_accel_path "<Actions>/view/view-zoom-fit-in" "<Primary>0")
(gtk_accel_path "<Actions>/dialogs/dialogs-gradients" "<Primary><Shift>g")
(gtk_accel_path "<Actions>/image/image-duplicate" "")
(gtk_accel_path "<Actions>/edit/edit-clear" "")
(gtk_accel_path "<Actions>/edit/edit-fill-fg" "<Alt>BackSpace")
(gtk_accel_path "<Actions>/tools/tools-crop" "c")
(gtk_accel_path "<Actions>/edit/edit-redo" "<Primary><Shift>z")
(gtk_accel_path "<Actions>/select/select-none" "<Primary>d")
(gtk_accel_path "<Actions>/context/context-brush-select-last" "greater")
(gtk_accel_path "<Actions>/layers/layers-raise" "<Primary>bracketright")
(gtk_accel_path "<Actions>/image/image-properties" "F8")
(gtk_accel_path "<Actions>/tools/tools-levels" "<Primary>l")
(gtk_accel_path "<Actions>/dialogs/dialogs-document-history" "<Primary><Shift>h")
(gtk_accel_path "<Actions>/tools/tools-eraser" "e")
(gtk_accel_path "<Actions>/view/view-show-guides" "<Primary>apostrophe")
(gtk_accel_path "<Actions>/file/file-export" "")
(gtk_accel_path "<Actions>/edit/edit-fill-bg" "<Primary>BackSpace")
(gtk_accel_path "<Actions>/dialogs/dialogs-colors" "F6")
(gtk_accel_path "<Actions>/image/image-print-size" "<Primary>p")
(gtk_accel_path "<Actions>/context/context-brush-select-first" "less")
(gtk_accel_path "<Actions>/tools/tools-blend" "g")
(gtk_accel_path "<Actions>/file/file-save-a-copy" "<Primary><Alt>s")
(gtk_accel_path "<Actions>/image/image-rotate-180" "8")
(gtk_accel_path "<Actions>/tools/tools-clone" "s")
(gtk_accel_path "<Actions>/context/context-brush-hardness-increase-skip" "braceright")
(gtk_accel_path "<Actions>/dialogs/dialogs-layers" "F7")
(gtk_accel_path "<Actions>/view/view-scroll-page-up" "Page_Up")
(gtk_accel_path "<Actions>/plug-in/file_print_gimp" "<Primary>p")
(gtk_accel_path "<Actions>/layers/layers-merge-down" "<Primary>e")
(gtk_accel_path "<Actions>/tools/tools-rect-select" "m")
(gtk_accel_path "<Actions>/view/view-scroll-page-down" "Page_Down")
(gtk_accel_path "<Actions>/tools/tools-bucket-fill" "<Shift>g")
(gtk_accel_path "<Actions>/image/image-rotate-90" "9")
(gtk_accel_path "<Actions>/layers/layers-mode-previous" "underscore")
(gtk_accel_path "<Actions>/layers/layers-preserve-transparency" "slash")
(gtk_accel_path "<Actions>/tools/tools-measure" "u")
(gtk_accel_path "<Actions>/tools/tools-cage" "")
(gtk_accel_path "<Actions>/tools/tools-paintbrush" "b")
(gtk_accel_path "<Actions>/tools/tools-dodge-burn" "o")
(gtk_accel_path "<Actions>/tools/tools-color-picker" "i")
(gtk_accel_path "<Actions>/view/view-show-selection" "<Primary>h")
(gtk_accel_path "<Actions>/tools/tools-free-select" "l")
(gtk_accel_path "<Actions>/tools/tools-move" "v")
(gtk_accel_path "<Actions>/view/view-info-window" "F8")
(gtk_accel_path "<Actions>/layers/layers-select-previous" "<Alt>bracketright")
(gtk_accel_path "<Actions>/context/context-brush-hardness-decrease-skip" "braceleft")
(gtk_accel_path "<Actions>/tools/tools-paint-brush-size-decrease" "bracketleft")
(gtk_accel_path "<Actions>/layers/layers-select-next" "<Alt>bracketleft")
(gtk_accel_path "<Actions>/layers/layers-anchor" "<Alt>h")
(gtk_accel_path "<Actions>/view/view-show-menubar" "<Shift>f")
(gtk_accel_path "<Actions>/drawable/drawable-desaturate" "<Primary><Shift>u")
(gtk_accel_path "<Actions>/plug-in/plug-in-c-astretch" "<Primary><Shift><Alt>l")
(gtk_accel_path "<Actions>/tools/tools-scale" "<Primary>t")
(gtk_accel_path "<Actions>/layers/layers-select-bottom" "<Alt>braceleft")
(gtk_accel_path "<Actions>/tools/tools-smudge" "")
(gtk_accel_path "<Actions>/tools/tools-hue-saturation" "<Primary>u")
(gtk_accel_path "<Actions>/edit/edit-fill-pattern" "")
(gtk_accel_path "<Actions>/tools/tools-value-2-decrease" "")
(gtk_accel_path "<Actions>/tools/tools-ellipse-select" "<Shift>m")
(gtk_accel_path "<Actions>/layers/layers-raise-to-top" "<Primary>braceright")
(gtk_accel_path "<Actions>/tools/tools-iscissors" "")
(gtk_accel_path "<Actions>/tools/tools-flip" "f")
(gtk_accel_path "<Actions>/view/view-show-rulers" "<Primary>r")
(gtk_accel_path "<Actions>/windows/windows-display-0006" "<Alt>1")
(gtk_accel_path "<Actions>/windows/windows-display-0009" "<Alt>9")
(gtk_accel_path "<Actions>/windows/windows-display-0008" "<Alt>8")
(gtk_accel_path "<Actions>/windows/windows-display-0007" "<Alt>7")
(gtk_accel_path "<Actions>/dialogs/dialogs-vectors" "F9")
(gtk_accel_path "<Actions>/quick-mask/quick-mask-toggle" "q")
(gtk_accel_path "<Actions>/dialogs/dialogs-palettes" "<Primary><Shift>l")
(gtk_accel_path "<Actions>/layers/layers-mask-add" "<Alt>o")
(gtk_accel_path "<Actions>/plug-in/script_fu_refresh" "<Primary><Shift><Alt>r")
(gtk_accel_path "<Actions>/edit/edit-paste-into" "<Primary><Shift>v")
(gtk_accel_path "<Actions>/tools/tools-fuzzy-select" "w")
(gtk_accel_path "<Actions>/view/view-zoom-out" "<Primary>minus")
(gtk_accel_path "<Actions>/dialogs/dialogs-preferences" "<Primary>k")"""

if __name__ == '__main__':
    if not sys.argv[1:]:
        write_gimp_menurc()
    if sys.argv[1] == 'macos':
        rewrite_info_plist()
        rename_app_dir()
