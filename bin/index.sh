#!/bin/sh
updatedb -n \*.pyc -n __pycache__ -n eggs -l 0 -o locatedb -U ./ &
pycscope.py -R src/ lib/ &
find . -name "*.py"|grep -v '#' | etags -D -I --output TAGS - &
