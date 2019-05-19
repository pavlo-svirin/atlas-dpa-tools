#!/bin/bash

[[ $# -eq 0 ]] && echo "Please give an ATLAS queue name" && exit 1

curl "http://atlas-agis-api.cern.ch/request/pandaqueue/query/list/?json&preset=full&panda_queue=$1"
