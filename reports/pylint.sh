#!/bin/bash

score="$(sed -n 's/^Your code has been rated at \([-0-9.]*\)\/.*/\1/p' ./reports/pylint.txt)"
anybadge --value=$(sed -n "s/^Your code has been rated at \([-0-9.]*\)\/.*/\1/p" ./reports/pylint.txt) --file=./reports/pylint.svg --overwrite pylint
