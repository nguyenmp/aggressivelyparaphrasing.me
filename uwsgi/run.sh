#!/bin/sh

# NearlyFreeSpeech prevents arguments in their UI so they recommend a "run" script
# https://members.nearlyfreespeech.net/faq?q=RunScript#RunScript

export SECRET_KEY=$(head -c 64 /dev/urandom | openssl enc -base64)
exec uwsgi --socket 127.0.0.1:3031 --wsgi scorsese --callable app --processes 4 --threads 2 --stats 127.0.0.1:9191 --logto /home/private/uwsgi.log
