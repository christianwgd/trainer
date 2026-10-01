#!/bin/bash

# Run schema migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start the server
gunicorn gunicorn -c config.py trainer.wsgi
