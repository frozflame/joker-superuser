unalias acd 2>/dev/null
function acd() {
    local IFS=$' \t\n'
    if [[ $1 == . ]]; then
        echo '# .' | netcat 127.0.0.1 8331
        return
    elif [[ -d "$*" ]]; then
        # shellcheck disable=SC2164
        cd "$*"
        return
    elif [[ -f "$*" ]]; then
        # shellcheck disable=SC2164
        cd "$(dirname "$*")"
        return
    fi

    case "$1" in
    :)
        shift
        $0 "$("$@")"
        return
        ;;
    which | where)
        shift
        $0 "$(command -v "$@")"
        return
        ;;
    git)
        # shellcheck disable=SC2164
        cd "$(git rev-parse --show-toplevel 2>/dev/null || echo .)"
        return
        ;;
    esac
    cd "$(echo "$*" | sed 's:\s:_:' | netcat 127.0.0.1 8331)" || return
}
