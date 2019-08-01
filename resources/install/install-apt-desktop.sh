if [[ $(id -u) != 0 ]]; then
    echo "You are not root."
    exit
fi

apt-get installl zsh
test -f ~/.oh-my-zsh/oh-my-zsh.sh || wget --no-check-certificate https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | sh
chsh -s /bin/zsh

apt-get install -y nginx
apt-get install -y imagemagick

apt-get install -y ubuntu-restricted-extras
apt-get install -y chromium-browser
apt-get install -y virtualbox
apt-get install -y language-pack-zh-hans

# tweak tools
apt-get install -y gnome-tweak-tool
apt-get install -y alacarte
apt-get install -y conf-editor

# web server

apt-get install -y gksu
apt-get install -y deluge

apt-get install -y xrdp     # remote desktop server
apt-get install -y ntfs-3g  # mount NTFS
apt-get install -y dnsutils # nslookup

# deluged bit-torrent solution
apt-get install -y deluged
apt-get install -y deluge-console
apt-get install -y python-mako
apt-get install -y deluge-web

# text
apt-get install -y pdfshuffler
apt-get install -y antiword
apt-get install -y enca

# others
apt-get install -y libqtwebkit-dev
apt-get install -y exiv2

# wireshark
apt-get install -y wireshark
dpkg-reconfigure wireshark-common

if [[ $1 ]]; then
    usermod -a -G wireshark "$1"
fi

# computing
apt-get install -y octave
apt-get install -y apcalc
apt-get install -y julia
apt-get install -y perl-console
apt-get install -y r-base-core

# image/audio/video editing
apt-get install -y krita
apt-get install -y darktable
apt-get install -y blender
apt-get install -y gimp
apt-get install -y inkscape

apt-get install -y ufraw-batch
apt-get install -y netpbm
apt-get install -y dcraw

# image/audio/video
apt-get install -y vlc
apt-get install -y mediainfo
apt-get install -y python-mutagen
# mp3 tag encode conversion: mid3iconv -e gbk --remove-v1 *.mp3

# convmv - converts filenames from one encoding to another
apt-get install -y convmv

# flash plugin
apt-get install -y pepperflashplugin-nonfree
update-pepperflashplugin-nonfree --install
