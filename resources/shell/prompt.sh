# http://zsh.sourceforge.net/Doc/Release/Prompt-Expansion.html
case "$(ps -p $$ -o comm= | sed 's:\W::')-$(( ${#SSH_CLIENT}  + ${#SSH_TTY} ? 1 : 0 ))" in
zsh-0)
    # %n = $USERNAME
    # %~ = $PWD, with leading $HOME or named directory replaced
    PS1=$'\n'
    PS1="$PS1"'%{$fg_bold[cyan]%}%n '
    PS1="$PS1"'%{$fg_bold[yellow]%}%~ '
    PS1="$PS1"'%{$fg_bold[blue]%}$(git_prompt_info)%{$fg_bold[green]%}'
    PS1="$PS1"$'\n'
    PS1="$PS1"'%{$fg_bold[green]%}\$ % '
    PS1="$PS1"'%{$reset_color%}'
    ;;
zsh-1)
    PS1=$'\n'
    PS1="$PS1"'%{$reset_color%}'
    PS1="$PS1"'%n@%M '
    PS1="$PS1"'%{$fg[yellow]%}%~ '
    PS1="$PS1"'%{$fg[blue]%}$(git_prompt_info)%{$fg[green]%}'
    PS1="$PS1"$'\n'
    PS1="$PS1"'%{$fg_bold[green]%}\$ % '
    PS1="$PS1"'%{$reset_color%}'
    ;;
bash-0)
    PS1CLR1=36
    PS1="\n\[\\e[${PS1CLR1}m\]\u\[\e[33m\] \w \[\e[0m\]\\$ "
    ;;
bash-1)
    # shellcheck disable=SC2154
    # shellcheck disable=SC2025
    export PS1="\n${debian_chroot:+($debian_chroot)}\u@\H \e[33m\w\e[0m \\$ "
    ;;
esac

