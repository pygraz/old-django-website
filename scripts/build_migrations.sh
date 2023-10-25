#!/bin/sh
set -ex
# TODO: Once the data model is reasonably stable, remove "rm" in order to preserve the data model.
rm -rf core/migrations/00*.py
rm -f pygraz.sqlite
poetry run python manage.py makemigrations --no-header
poetry run python manage.py make_demo
