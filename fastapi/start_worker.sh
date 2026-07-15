#!/bin/sh

# Check if the queue name is provided as an argument
if [ -z "$1" ]; then
    echo "Error: Queue name is required."
    exit 1
fi

celery -A app.celery_app:celery worker -l debug -Q $1 --pool threads --concurrency 5 -n celery_worker@%h --without-mingle -Ofair
