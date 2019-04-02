#!/bin/bash

shopt -s extglob

[[ -z "$1" ]] && echo No site specified && exit 1
SITE=$1
HOURS=${2:-12}

echo Opening ${SITE} with its stats for ${HOURS}

RESOURCETYPE=$((tr '/' '\n' | tail -n +2) <<< ${SITE} )
SITENAME=$((tr '/' '\n' | head -n 1) <<< ${SITE} )

[[ ! -z "${RESOURCETYPE}" ]] && RESOURCETYPE="&resourcetype=${RESOURCETYPE}"

SITEURL="https://bigpanda.cern.ch/jobs/?computingsite=${SITENAME}&jobtype=production&jobstatus=failed&hours=${HOURS}&display_limit=100${RESOURCETYPE}"


osascript -e "tell application \"Firefox\"
	activate
end tell

tell application \"Firefox\"
	open location \"${SITEURL}\"
end tell"
