#!/bin/bash
# Railway startup script for Portfolio Manager

# Set Python path to include root directory for shared module access
export PYTHONPATH=/app:$PYTHONPATH

# Change to app directory
cd /app/app1_portfolio_manager

# Start gunicorn
exec gunicorn app:app \
  --bind 0.0.0.0:$PORT \
  --workers 2 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile -
