web: gunicorn zorpido_config.wsgi:application --workers 3 --worker-class sync --worker-tmp-dir /dev/shm --bind 0.0.0.0:$PORT --access-logfile - --error-logfile - --log-level info
