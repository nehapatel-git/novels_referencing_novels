#!/bin/bash

#get the absolute path of the directory that the repo is in
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)"

# use the venv to run the script
"$DIR/.venv/bin/python" "$DIR/update_network.py"
