# shellcheck disable=SC2164
unalias acd 2>/dev/null
function acd() {
    local IFS=$' \t\n'

    case "$1" in
    :)
        shift
        cd "$("$@")"
        return
        ;;
    which | where)
        shift
        cd "$(command -v "$@")"
        return
        ;;
    git)
        cd "$(git rev-parse --show-toplevel 2>/dev/null || echo .)"
        return
        ;;
    *)
        set -- "$*"
        ;;
    esac

    if [[ -d $1 ]]; then
        cd "$1"
        return
    elif [[ -f $1 ]]; then
        cd "$(dirname "$1")"
        return
    fi

    case "$1" in
    .)
        echo '# .' | netcat 127.0.0.1 8331 2>/dev/null
        return
        ;;
    '~')
        cd
        return
        ;;
    '~'/*)
        cd "${1/#\~\//${HOME}/}"
        return
        ;;
    esac

    local TargetDir
    TargetDir="$(echo "$1" | sed 's:\s:_:' | netcat 127.0.0.1 8331 2>/dev/null)"
    if [[ $TargetDir ]]; then
        cd "$TargetDir"
        return
    fi

    case $1 in
    l)
        cd /var/log
        ;;
    a)
        cd /etc/apache2
        ;;
    aa)
        cd /etc/apache2/sites-available
        ;;
    ae)
        cd /etc/apache2/sites-enabled
        ;;
    ssh)
        cd ~/.ssh/
        ;;
    n)
        cd /etc/nginx
        ;;
    na)
        cd /etc/nginx/sites-available
        ;;
    ne)
        cd /etc/nginx/sites-enabled
        ;;
    ns)
        cd /etc/nginx/servers
        ;;
    nl)
        cd /var/log/nginx/
        ;;
    su)
        cd /etc/supervisor/conf.d
        ;;
    esac
}
