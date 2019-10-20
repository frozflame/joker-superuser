#!/usr/bin/env bash

if [[ $(id -u) != 0 ]]; then echo "You are not root."; exit; fi

set -e
set -x

apt-get remove docker docker-engine docker.io containerd runc
apt-get update
apt-get install apt-transport-https ca-certificates curl  gnupg-agent  software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
apt-key fingerprint 0EBFCD88
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

apt-get update
apt-get install docker-ce docker-ce-cli containerd.io
docker run hello-world


# run docker as non-root
if [[ $1 ]]; then sudo usermod -a -G docker "$1"; fi
