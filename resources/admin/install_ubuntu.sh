if [[ $(id -u) != 0 ]]; then
    echo "You are not root."
    exit
fi

apt-get installl zsh
test -f ~/.oh-my-zsh/oh-my-zsh.sh || wget --no-check-certificate https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | sh
chsh -s /bin/zsh

apt-get install -y moreutils
apt-get install -y vim
apt-get install -y tree
apt-get install -y iotop
apt-get install -y fdupes
apt-get install -y p7zip-full
apt-get install -y lsof
apt-get install -y tmux
apt-get install -y ntfs-3g      # mount NTFS
apt-get install -y dnsutils     # nslookup

