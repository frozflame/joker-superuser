#!/usr/bin/env bash

# https://ubuntubudgie.org/blog/2017/06/04/how-to-enable-global-menus-in-ubuntu-budgie

if [[ $(id -u) != 0 ]]; then echo "You are not root."; exit; fi
add-apt-repository ppa:ubuntubudgie-dev/global-menu-test
apt-get update
apt install budgie-pixel-saver-applet budgie-appmenu-applet
echo "Logout and then back in to see the new applets in Raven."
