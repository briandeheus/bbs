#!/usr/bin/env bash

source .venv/bin/activate
daphne messageboard.asgi:application
