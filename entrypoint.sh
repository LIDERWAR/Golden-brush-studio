#!/bin/sh
set -e

if [ -n "$POSTGRES_HOST" ]; then
  echo "Waiting for PostgreSQL ($POSTGRES_HOST:$POSTGRES_PORT)..."
  while ! python -c "import socket; s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.connect(('$POSTGRES_HOST', int('$POSTGRES_PORT'))); s.close()" 2>/dev/null; do
    sleep 1
  done
  echo "PostgreSQL is ready!"
fi

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

if [ "$AUTO_SEED_DB" = "true" ] || [ "$AUTO_SEED_DB" = "1" ]; then
  echo "Auto-seeding database (superuser, demo projects & artworks)..."
  python seed_db.py || true
fi

exec "$@"
