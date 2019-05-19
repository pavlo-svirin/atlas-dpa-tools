#!/bin/bash

tempfoo=`basename $0`
TMPFILE=`mktemp /tmp/${tempfoo}.XXXXXX` || exit 1


function join { local IFS="$1"; shift; echo "$*"; }


cat > ${TMPFILE} << EOF
Description: 
Example: 
Sites: 
GGUS: 
Comment: 
EOF

vim ${TMPFILE}

DESCRIPTION=
EXAMPLES=
SITES=

while read i; do
    KW=$(grep -o -E '^[A-Za-z]+:' <<< "$i")
    case "${KW}" in
        Description:) 
                        DESCRIPTION=$(sed 's/Description: //' <<< "$i" )
                        ;;
        Example:) 
                        EXAMPLES=($(sed 's/Example: //' <<< "$i")) #| ( while read k; do echo -n '[[' $k ']]' ; done ))
                        EXAMPLES=$(join , $(for e in "${EXAMPLES[@]}"; do echo -n "[[$e]] "; done))
                        ;;

        Sites:) 
                        SITES=($(sed 's/Sites: //' <<< "$i"))
                        SITES=$(join , ${SITES[@]})
                        ;;
        GGUS:) 
                        TICKET_ID=$(sed 's/GGUS: //' <<< "$i") 
                        GGUS_TICKET="[[https://ggus.eu/?mode=ticket_info&ticket_id=${TICKET_ID}][${TICKET_ID}]]"
                        ;;
        Comment:) ;;
    esac
done < ${TMPFILE}

if [[ ! -z "${GGUS_TICKET}" ]]; then
    STATUS="Ticket created"
else
    STATUS="Observation"
fi

rm -f ${TMPFILE}

cat << EOF


            * ${DESCRIPTION}
               * Status: ${STATUS}
               * Example: ${EXAMPLES}
               * GGUS: ${GGUS_TICKET}
               * Sites: ${SITES}
               * Comment: ${COMMENT}


EOF
