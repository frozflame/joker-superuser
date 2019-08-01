unalias acd 2>/dev/null
function acd() {
    local IFS=$' \t\n'
    local DIR

    case "$1" in
    :)
        shift
        # shellcheck disable=SC2164
        cd "$("$@")"
        return
        ;;
    which | where)
        shift
        # shellcheck disable=SC2164
        cd "$(command -v "$@")"
        return
        ;;
    git)
        # shellcheck disable=SC2164
        cd "$(git rev-parse --show-toplevel 2>/dev/null || echo .)"
        return
        ;;
    *)
        DIR="$*"
        ;;
    esac

    if [[ -d $DIR ]]; then
        # shellcheck disable=SC2164
        cd "$DIR"
        return
    elif [[ -f $DIR ]]; then
        # shellcheck disable=SC2164
        cd "$(dirname "$DIR")"
        return
    fi

    case "$DIR" in
    .)
        echo '# .' | netcat 127.0.0.1 8331
        return
        ;;
    '~')
        # shellcheck disable=SC2164
        cd
        return
        ;;
    '~'/*)
        # shellcheck disable=SC2164
        cd "${DIR/#\~\//${HOME}/}"
        return
        ;;
    esac
    cd "$(echo "$DIR" | sed 's:\s:_:' | netcat 127.0.0.1 8331)" || return
}
