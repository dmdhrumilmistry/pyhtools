#!/bin/bash

# exit when error occurs
set -e 

# install twine if not installed
if [ $(python -m pip list | grep twine | tr -s [:space:] | wc -w) -ne 2 ]; then
    python -m pip install twine
fi 

# remove dist directory if already exists
if [ -d "dist" ]; then rm -rf "dist"; fi

# create dist wheels
python setup.py build sdist bdist_wheel

# twine has -u and -p operator to pass username and passsword via command 
# line but its not preferred to pass username and password via cli 

# upload to pypi using twine
python -m twine upload dist/*

# now enter username and password