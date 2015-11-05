#!/usr/bin/env bash
set -e

python3 -m venv ./virtual/arelle
echo "Virtualenv created"
source ./virtual/arelle/bin/activate
echo "Virtualenv activated"

pip install lxml==3.4.4
python setup.py sdist
