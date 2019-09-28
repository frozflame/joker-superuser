# zwc - wc gzipped files
# http://stackoverflow.com/a/846077/2925169
function zwc() {
    for F in "$@"; do
        echo "$(zcat -f <"$F" | wc -l) $F"
    done
}
