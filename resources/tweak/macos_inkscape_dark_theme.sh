function _backup {
    test -f "$1" && cp -i "$1" "$1.bak"
}

function _restore {
    test -f "$1" && cp -i "$1" "${1#.bak}"
}

# https://github.com/abirnie/inkscape-dark-theme-mac
# http://www.mediafire.com/file/bunqu4bqt88bzqa/Inkscape+0.91+dark+theme.zip
function _inkscape_theme_dark {
    _backup /Applications/Inkscape.app/Contents/Resources/etc/gtk-2.0/gtkrc
    curl https://raw.githubusercontent.com/frozflame/jokerseries/joker-superuser/resources/tweak/gtkrc-inkscape-dark-theme.txt > /Applications/Inkscape.app/Contents/Resources/etc/gtk-2.0/gtkrc
}

function _inkscape_theme_restore {
    _restore /Applications/Inkscape.app/Contents/Resources/etc/gtk-2.0/gtkrc.bak
}

