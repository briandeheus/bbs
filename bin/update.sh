#!/usr/bin/env bash

echo "Updating your BBS..."

source .venv/bin/activate

git pull origin master

npm ci
npx tailwindcss -o ./messageboard/static/messageboard/styles/styles.css

pip install -r requirements.txt --extra-index-url "https://dl.fontawesome.com/$FONTAWESOME_TOKEN/fontawesome-pro/python/simple/"

./manage.py migrate
./manage.py collectstatic --no-input -v3 \
            --ignore fontawesomepro/svgs/* \
            --ignore fontawesomepro/js-packages/*
