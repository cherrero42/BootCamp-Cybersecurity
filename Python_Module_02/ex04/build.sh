#!/usr/bin/env bash

## Usage:
# python -m venv tmp_env && source tmp_env/bin/activate
# bash ./build.sh

### Make sure you have the latest versions of setuptools and wheel installed:
# python -m pip install --upgrade pip setuptools wheel

python3 setup.py sdist bdist_wheel

pip install ./dist/my_minipack-1.0.1.tar.gz
