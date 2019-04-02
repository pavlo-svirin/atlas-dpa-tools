#!/usr/bin/env python3

from core.net.curl import Curl

if __name__ == "__main__":
    curl = Curl()
    print(curl.perform('https://bigpanda.cern.ch/errorslist/?codename=jobdispatchererrorcode&codeval=100&tk=735147&json'))
    curl.close()
