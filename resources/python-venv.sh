#!/usr/bin/env bash

# venv activation
function ve() {
    if [[ ${VIRTUAL_ENV} ]]; then deactivate; return; fi

    declare -a ARR=()
    while IFS= read -r -d $'\0'; do
        ARR+=("$REPLY")
    done < <(find . -path "*/bin/activate" -print0)
    set -- "${ARR[@]}"

    if [[ $# -eq 0 ]]; then return; fi
    if [[ $# -gt 1 ]]; then
        echo "$# activation scripts found:"
        for s; do echo "$s"; done
        return
    fi

    if [[ $PS1 == $'\n'* ]]; then
        set -- "$1" $'\n'
    elif [[ $PS1 == '\n'* ]]; then
        set -- "$1" '\n'
    fi

    # shellcheck disable=SC1090
    source "$1"
    export PS1="${2}${PS1}"
}
