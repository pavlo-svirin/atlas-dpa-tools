#!/bin/bash

curl "http://atlasdistributedcomputing-live.web.cern.ch/ATLASDistributedComputing-live/#Pilots" | pup 'script' | sed -n '/var pilot/,/];/p' | sed -e '1d' -e '$d' | sed -E -e 's/^[[:space:]]+\[//' -e 's/\],?[[:space:]]*$//'
