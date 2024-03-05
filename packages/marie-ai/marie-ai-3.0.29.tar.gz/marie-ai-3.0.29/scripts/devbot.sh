#!/bin/bash

set -e

# this script is run by marie-dev-bot

# inject @overload info && black it
arr=( $(python inject-cli-as-overload.py) ) && black -S "${arr[@]}"
arr=( $(PYTHONPATH=.. python inject-document-props-as-overload.py) ) && black -S "${arr[@]}"

# update autocomplete info && black it
python update-autocomplete-cli.py && black -S ../marie_cli/autocomplete.py
python generate-list-args.py


# sync package requirements with resources/ requirements
cp ../extra-requirements.txt ../marie/resources/