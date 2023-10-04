#!/usr/bin/env bash

echo "Updating your BBS..."

git pull origin master

./manage.py migrate
./manage.py collectstatic --no-input
