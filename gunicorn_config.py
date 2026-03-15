"""
Gunicorn WSGI configuration for ReThread production deployment
Run with: gunicorn -c gunicorn_config.py app:app
"""

import multiprocessing
import os

# Number of worker processes (2 x CPU cores + 1)
workers = multiprocessing.cpu_count() * 2 + 1

# Worker class (sync for CPU-bound tasks, gevent for I/O-bound)
worker_class = "sync"

# Maximum number of connections per worker
worker_connections = 1000

# Timeout for workers (seconds)
timeout = 30

# Keep-alive timeout (seconds)
keepalive = 2

# Bind address and port
bind = "0.0.0.0:5000"

# Access log format
accesslog = "-"

# Error log format
errorlog = "-"

# Log level
loglevel = "info"

# Max request size
max_requests = 1000

# Max request jitter to prevent thundering herd
max_requests_jitter = 50

# Graceful timeout (seconds)
graceful_timeout = 30

# Reload workers when code changes (development only)
# reload = False  # Set to True only in development
