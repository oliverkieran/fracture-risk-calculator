#!/usr/bin/env bash
# exit on error
set -o errexit

# install dependencies
python3 -m pip install -r requirements.txt

# run migrations
python manage.py migrate