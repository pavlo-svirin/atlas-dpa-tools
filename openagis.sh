#!/bin/bash

shopt -s extglob

[[ -z "$1" ]] && echo No site specified && exit 1

SITEURL="https://atlas-agis.cern.ch/agis/pandaqueue/detail/$1/full/"


osascript -e "tell application \"Firefox\"
	activate
end tell

tell application \"Firefox\"
	open location \"${SITEURL}\"
end tell"
