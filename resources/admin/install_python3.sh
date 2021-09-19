#!/usr/bin/env bash

if [[ $(id -u) != 0 ]]; then
    echo "You are not root."
    exit
fi

# https://packaging.python.org/guides/installing-using-linux-tools/

if command -v apt-get >/dev/null; then
    apt-get install -y python3 python3-pip
elif command -v dnf >/dev/null; then
    dnf install python3
elif command -v pacman >/dev/null; then
    pacman -S python-pip
elif command -v zypper >/dev/null; then
    zypper install python3-pip
fi

python3 -m pip install virtualenv

# Fedora users: https://developer.fedoraproject.org/tech/languages/python/multiple-pythons.html
