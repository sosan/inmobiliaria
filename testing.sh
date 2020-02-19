#!/bin/sh
set -e
if [ "${FLASK_ENV}" = "development" ]; then
    echo "FLASK_ENV POR DEFECTO: development"
    # exec "$@"
else
    echo "FLASK_ENV POR DEFECTO: production"
    # exec gunicorn -b 0.0.0.0:${PORT} app
fi

exec "$@"
# shellcheck
# No issues detected!