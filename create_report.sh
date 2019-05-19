#!/bin/bash

WEEKDAY=$(gdate +"%w")

DATE=$(gdate --date="+1 days" +"%d/%m/%Y")


[[ $WEEKDAY -eq 5 ]] && DATE=$(gdate --date="+3 days" +"%d/%m/%Y")
[[ $WEEKDAY -eq 6 ]] && DATE=$(gdate --date="+2 days" +"%d/%m/%Y")
[[ $WEEKDAY -eq 0 ]] && DATE=$(gdate --date="+1 days" +"%d/%m/%Y")

tempfoo=`basename $0`
TMPFILE=`mktemp /tmp/${tempfoo}.XXXXXX` || exit 1

vim ${TMPFILE}

cat << EOF
${DATE}

      * Errors - [[https://docs.google.com/document/d/1nDlRS6PsNIfhsjxoVKTgI0Y-IQIdVTqKmcWkRJ6EzHg/edit?usp=sharing][link]]
         * New

	 * Follow-ups:
$(grep -E '(^\s{11,}|^\s*$)' ${TMPFILE})
EOF


rm -f ${TMPFILE}
