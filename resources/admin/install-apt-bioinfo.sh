#!/usr/bin/env bash
if [[ $(id -u) != 0 ]]; then echo "You are not root."; exit; fi

apt-get install -y mrbayes
apt-get install -y mcl
apt-get install -y ncbi-blast+
apt-get install -y tigr-glimmer
apt-get install -y emboss
apt-get install -y clustalw
apt-get install -y clustalo
apt-get install -y ugene
