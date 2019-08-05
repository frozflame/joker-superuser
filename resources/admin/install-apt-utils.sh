
if [[ $(id -u) != 0 ]]; then echo "You are not root."; exit; fi

apt-get install -y moreutils
apt-get install -y vim
apt-get install -y tree
apt-get install -y iotop
apt-get install -y fdupes
apt-get install -y p7zip-full
apt-get install -y lsof
apt-get install -y tmux



