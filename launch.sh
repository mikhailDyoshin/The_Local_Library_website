#!/bin/bash

sudo apt-get install python3-venv

python3 -m venv .venv

source .venv/bin/activate

python -m pip install --upgrade pip

pip install -r requirements.txt