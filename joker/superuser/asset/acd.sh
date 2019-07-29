unalias acd 2>/dev/null
function acd() {
    if [[ $1 == . ]]; then
        echo '# .' | netcat 127.0.0.1 8330
        return
    elif [[ -d $1 ]]; then
        # shellcheck disable=SC2164
        cd "$1"
        return
    elif [[ -f $1 ]]; then
        # shellcheck disable=SC2164
        cd "$(dirname "$1")"
        return
    fi

    case "$1" in
    :)
        shift
        $0 "$("$@")"
        return
        ;;
    where|which)
        $0 "$("$@")"
        return
        ;;
    git)
        # shellcheck disable=SC2164
        cd "$(git rev-parse --show-toplevel 2>/dev/null || echo .)"
        return
        ;;
    esac

    cd "$(echo "$1" | sed 's:\s:_:' | netcat 127.0.0.1 8330)" || return
}
