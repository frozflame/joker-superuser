#!/usr/bin/env bash

if [[ $(id -u) != 0 ]]; then echo "You are not root."; exit; fi

apt install -y vim
update-alternatives --install /usr/bin/editor editor /usr/bin/vim 1
update-alternatives --set editor /usr/bin/vim
update-alternatives --install /usr/bin/vi vi /usr/bin/vim 1
update-alternatives --set vi /usr/bin/vim

function append {
    if [[ -f $2 ]]; then
        grep ^"$1"  "$2" > /dev/null || echo "$1" >> "$2"
    fi
}

append "export EDITOR=vim" ~/.bashrc
append "export EDITOR=vim" ~/.zshrc
