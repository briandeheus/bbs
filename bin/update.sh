#!/usr/bin/env bash

echo "Updating your BBS..."

source .venv/bin/activate

git pull origin master

npm ci
npx tailwindcss -o ./messageboard/static/messageboard/styles/styles.css

./manage.py migrate
./manage.py collectstatic --no-input
