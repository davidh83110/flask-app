#!/bin/bash

# We need to make sure Redis is start before Flask.
REDIS_HOST="${REDIS_HOST:-127.0.0.1}"
MAX_RETRIES=60
RETRY_COUNT=0
until redis-cli -h "$REDIS_HOST" ping; do
  RETRY_COUNT=$((RETRY_COUNT + 1))
  if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
      echo "Timeout: Redis server did not start after $MAX_RETRIES retries."
      exit 1
  fi
  echo "Waiting for Redis server to start... (Attempting: $RETRY_COUNT)"
  sleep 1
done

echo "Redis server is up and running."


# Load the history data if exist.
if [ -f /data/history_data.json ]; then
    echo "Found history_data.json, hence start loading data into Redis..."
    python /migrations.py
fi

: "${GUNICORN_BIND:=0.0.0.0:3000}"
: "${GUNICORN_WORKERS:=1}"
: "${GUNICORN_ACCESS_LOG:=-}"   # default to STDOUT
: "${GUNICORN_ERROR_LOG:=-}"    # default to STDERR
: "${GUNICORN_GRACEFUL_TIMEOUT:=30}"

# Start Gunicorn
exec gunicorn --bind "$GUNICORN_BIND" \
              --workers "$GUNICORN_WORKERS" \
              --access-logfile "$GUNICORN_ACCESS_LOG" \
              --error-logfile "$GUNICORN_ERROR_LOG" \
              --logger-class 'utils.logger.GunicornJsonLogger' \
              --graceful-timeout "$GUNICORN_GRACEFUL_TIMEOUT"\
              wsgi:app

