unalias acd 2>/dev/null
function acd {
    set -e
    case $1 in
        w)
            cd /data/www
            ;;
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
        s|ssh)
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
