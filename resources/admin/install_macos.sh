if [[ $1 == uninstall-brew ]]; then
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/uninstall)"
    exit
fi

# install brew
command -v brew || test -f /usr/local/bin/brew ||  ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

brew install zsh
#export PATH="$(brew --prefix coreutils)/libexec/gnubin:/usr/local/bin:$PATH"

test -f ~/.oh-my-zsh/oh-my-zsh.sh || wget --no-check-certificate https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | sh
chsh -s /bin/zsh

brew install file-formula
brew install git
brew install less
brew install openssh
brew install python
brew install rsync
brew install unzip
brew install unar # The unarchiver CLI
brew install vim --override-system-vi

# GNU utils
brew install bash
brew install gdb # gdb requires further actions to make it work. See `brew info gdb`.
brew install coreutils
brew install gpatch
brew install make
brew install binutils
brew install diffutils
brew install ed
brew install findutils
brew install gawk
brew install gnu-indent
brew install gnu-sed
brew install gnu-tar
brew install gnu-which
brew install gnutls
brew install grep
brew install gzip
brew install tmux
brew install watch
brew install gettext
brew install wget
brew install netcat
