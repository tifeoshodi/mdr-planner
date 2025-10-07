#!/bin/bash
set -e

echo "Starting Portfolio Manager..."
echo "Current directory: $(pwd)"
echo "PYTHONPATH before: $PYTHONPATH"

# Set Python path to include parent directory
export PYTHONPATH=/app:$PYTHONPATH

echo "PYTHONPATH after: $PYTHONPATH"
echo "Changing to app directory..."

cd app1_portfolio_manager

echo "Now in: $(pwd)"
echo "Starting gunicorn..."

exec gunicorn app:app \
  --bind 0.0.0.0:$PORT \
  --workers 2 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile -
