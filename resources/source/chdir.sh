# shellcheck disable=SC2164

true "${JOKER_SUPERUSER_ABBRMAP_PORT:=8331}"

unalias acd 2>/dev/null
function acd() {
    local IFS=$' \t\n'

    # get command output or join with spaces
    case "$1" in
    --)
        # use plain cd
        \cd -- "$@"
        return
        ;;
    :)
        set -- "$("$@")"
        ;;
    which | where)
        shift
        set -- "$(command -v "$@")"
        ;;
    *)
        set -- "$*"
        ;;
    esac

    # psudo-locations and special locations
    case "$1" in
    .)
        echo '#update' | netcat 127.0.0.1 $JOKER_SUPERUSER_ABBRMAP_PORT 2>/dev/null
        return
        ;;
    '~')
        \cd
        return
        ;;
    '~'/*)
        set -- "${1/#\~\//${HOME}/}"
        ;;
    git)
        \cd "$(git rev-parse --show-toplevel 2>/dev/null || echo .)"
        return
        ;;
    esac

    # existing file or directory
    if [[ -d $1 ]]; then
        \cd "$1"
        return
    elif [[ -f $1 ]]; then
        \cd "$(dirname "$1")"
        return
    elif [[ $1 =~ -[0-9]+ ]]; then
        # shellcheck disable=SC2086
        \cd "$(yes ../ | head -n 64 | head -n ${1#-} | tr -d '\n')"
    fi

    # lookup
    local TargetDir
    TargetDir="$(echo "$1" | sed 's:\s:_:' | netcat 127.0.0.1 $JOKER_SUPERUSER_ABBRMAP_PORT 2>/dev/null)"
    if [[ $TargetDir ]]; then
        \cd "$TargetDir"
        return
    fi

    # presets
    case $1 in
    sus)
        \cd ~/.joker/superuser/
        ;;
    l)
        \cd /var/log
        ;;
    a)
        \cd /etc/apache2
        ;;
    aa)
        \cd /etc/apache2/sites-available
        ;;
    ae)
        \cd /etc/apache2/sites-enabled
        ;;
    ssh)
        \cd ~/.ssh/
        ;;
    n)
        \cd /etc/nginx
        ;;
    na)
        \cd /etc/nginx/sites-available
        ;;
    ne)
        \cd /etc/nginx/sites-enabled
        ;;
    ns)
        \cd /etc/nginx/servers
        ;;
    nl)
        \cd /var/log/nginx/
        ;;
    su)
        \cd /etc/supervisor/conf.d
        ;;
    esac
}
