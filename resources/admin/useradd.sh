#!/usr/bin/env bash

read -r -d '' usage <<EOT
usage:
\$ $0 trump
\$ $0 trump su
EOT

if [[ $# -eq 0 ]]; then
    set -- -h
    cat "$0"
fi

if [[ $1 == -h ]]; then
    echo -e "$usage" >&2
    exit
fi

# ---------------------------------------------------------

set -x
set -e
[[ $1 == -h ]] && exit

echo pigs
exit

if [[ $(id -u) != 0 ]]; then
    echo "You are not root."
    exit
fi

username=$1
userdir=/home/${username}

usermod -s /bin/bash "${username}"
mkdir -p "${userdir}"/.ssh
touch "${userdir}"/.ssh/authorized_keys

# login ---------------------------------------------------
chmod 700 "${userdir}"/.ssh
chmod 600 "${userdir}"/.ssh/authorized_keys
chown "${username}":"${username}" -R ${userdir}

if [[ $2 == su ]]; then
    usermod -a -G sudo "${username}"
fi

echo "Set password for user ${username}:"
passwd "${username}"
