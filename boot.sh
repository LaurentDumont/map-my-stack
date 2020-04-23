#!/bin/sh
cd app/ && exec gunicorn -b :5001 --reload --workers=5 --threads=2 --access-logfile - --error-logfile - map-my-stack:app
 