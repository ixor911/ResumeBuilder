#!/usr/bin/env sh
set -e

if [ "$DB_ENGINE" = "postgres" ]; then
  python - <<'PY'
import os
import socket
import time

host = os.environ.get("DB_HOST", "db")
port = int(os.environ.get("DB_PORT", "5432"))
timeout = int(os.environ.get("DB_WAIT_TIMEOUT", "30"))
deadline = time.time() + timeout

while True:
    try:
        with socket.create_connection((host, port), timeout=2):
            break
    except OSError:
        if time.time() >= deadline:
            raise
        time.sleep(1)
PY
fi

if [ "$DJANGO_AUTO_MIGRATE" = "1" ]; then
  python manage.py migrate --noinput
fi

if [ "$DJANGO_COLLECTSTATIC" = "1" ]; then
  python manage.py collectstatic --noinput
fi

exec "$@"
