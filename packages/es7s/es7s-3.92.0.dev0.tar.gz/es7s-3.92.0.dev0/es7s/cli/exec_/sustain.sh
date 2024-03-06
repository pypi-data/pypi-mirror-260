#!/bin/bash
#-------------------------------------------------------------------------------
# es7s/core | endlessly (re)run a specified command, measure time and max memory
# (c) 2023 A. Shavykin <0.delameter@gmail.com>
#-------------------------------------------------------------------------------
__SELF="$(basename "$0" | sed -Ee 's/\..+$//')"
__USAGE="$(cat <<-EOL
Endlessly run the specified COMMAND with ARGS, keep track of launch count and
latest exit code.

USAGE:
  ${__SELF} [-d DELAY] [--overlay] [--confirm] [COMMAND [ARGS...]]

OPTIONS:
  -d DELAY     Set waiting interval between runs to DELAY seconds, where DELAY is a floating-point number. Specify 0 to disable the waiting.
  --overlay    Do not clear terminal before each run
  --confirm    Require a key press after each run
EOL
)"

__now() { date $'+\e[2m%_e-%b\e[22;33m %R\e[39m' ; }
__exit() { printf "\x1b[2J\x1b[H" >&2 ; exit ; }
__main () {
    trap __exit INT

    local restarts=0
    [[ $# -lt 1 ]] && set who #last -n$(($(tput lines)-5))

    while true ; do
        if [[ -z $ARG_OVERLAY ]] || [[ $restarts -eq 0 ]] ; then
            printf "\x1b[2J" >&2
        fi
        printf "\x1b[H" >&2
        [[ $excess -gt $(( -1 * (( totallen + ${#cmdlen} + 3 )) )) ]] && echo

#       .......................................................
        /usr/bin/time -o /tmp/sustain -f $'\x1c'"%E %M %x" "$@"
#       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        [[ -n $ARG_CONFIRM ]] \
          && printf 'Continue? (y/\x1b[4mn\x1b[24m): ' >&2 \
          && read -r -n1 yn >&2 \
          && case "$yn" in [Yy]*) ;; *) exit ;; esac

        local tstr="$(grep -Ee $'^\x1c' -m1 /tmp/sustain)"
        local rstr=$restarts ; [[ $restarts -gt 999 ]] && rstr=${restarts:0:-3}K
        local cmd="$(tr '\n' ' ' <<< "$*")"
        local totallen=$(( 16 + ${#cmd} + ${#rstr} + ${#tstr} +4))
        local excess=$(( $totallen - $(tput cols) ))
        local cmdlen=$(( ${#cmd} - $excess ))
        local cmdstr=""; [[ $cmdlen -gt 0 ]] && cmdstr="${cmd:0:$cmdlen}"
        printf "\x1b[H\x1b[9999G\x1b[${totallen}D\x1b[90;2m%s \x1b[34;22;1;48;5;17m %s \x1b[22;34;48;5;16m %s \x1b[m" "$cmdstr" "$rstr" "$(__now)" >&2
        printf "%s %skb [%s]" $tstr >&2

        [[ -n $ARG_DELAY ]] && sleep $ARG_DELAY
        ((restarts++))
    done
}

[[ $* =~ (--)?help ]] && echo "$__USAGE" && exit

declare ARG_DELAY=1.0
declare ARG_OVERLAY=
declare ARG_CONFIRM=

while true ; do
  if [[ $1 == -d ]] ; then
      ARG_DELAY=$2 && shift 2
      [[ $ARG_DELAY =~ ^\s*0*\.0*\s*$ ]] && ARG_DELAY=
      continue
  fi
  [[ $1 == --overlay ]] && ARG_OVERLAY=true && shift && continue
  [[ $1 == --confirm ]] && ARG_CONFIRM=true && shift && continue
  break
done

__main "$@"
