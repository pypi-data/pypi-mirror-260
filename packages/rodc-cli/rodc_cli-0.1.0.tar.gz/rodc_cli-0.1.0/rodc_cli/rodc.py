#!/usr/bin/env python3

import os
import sys

import requests

def cli():
    key = os.environ["RODC_API_KEY"]
    target = os.environ["RODC_TARGET"]
    if len(sys.argv) < 2:
        print("rodc-cli: not enough arguments")
        sys.exit(1)
    if sys.argv[1] == "-f":
        assert len(sys.argv) == 3
        r = requests.put(target + "/sf/" + sys.argv[2],
                         headers={"X-RODC-Authentication": key},
                         data=open(sys.argv[2]).read())
        print(r.status_code, r.text)
    else:
        assert len(sys.argv) == 2
        r = requests.put(target + "/s/" + sys.argv[1].split(".")[-1],
                         headers={"X-RODC-Authentication": key},
                         data=open(sys.argv[1]).read())
        print(r.status_code, r.text)

if __name__ == "__main__":
    cli()
