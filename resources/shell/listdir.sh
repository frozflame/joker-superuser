# shellcheck disable=SC2139

# Replace Mac OS X utilities with GNU core utilities - Unified Solution
# http://apple.stackexchange.com/a/69332/103216
if [[ $(/usr/local/bin/guname -o 2>/dev/null) == Darwin ]]; then
    if [[ -d /usr/local/opt/coreutils/libexec/gnubin ]]; then
        export PATH=/usr/local/opt/coreutils/libexec/gnubin:"$PATH"
    fi
    if [[ -d /usr/local/opt/coreutils/libexec/gnuman ]]; then
        export MANPATH=/usr/local/opt/coreutils/libexec/gnuman:"${MANPATH-/usr/share/man}"
    fi
    GNULS="$(command -v gls)"
else
    GNULS='/bin/ls'
fi

if [[ $GNULS ]]; then
    alias ls="${GNULS} --group-directories-first -F"
    alias LS="${GNULS} --group-directories-first -Ftr"
    alias ll="${GNULS} --group-directories-first -Fl"
    alias lh="${GNULS} --group-directories-first -Flh"
    alias li="${GNULS} --group-directories-first -Fli"
    alias la="${GNULS} --group-directories-first -FA"
    alias gnuls="${GNULS}"
else
    alias ls="/bin/ls -F"
    alias LS="/bin/ls -Ftr"
    alias ll="/bin/ls -Fl"
    alias lh="/bin/ls -Flh"
    alias li="/bin/ls -Fli"
    alias la="/bin/ls -FA"
    alias lo="/bin/ls -Ol"
fi
