# based on https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker

import multiprocessing
import os

host = os.getenv("HOST", "0.0.0.0")
port = os.getenv("PORT", "9000")
bind_env = os.getenv("BIND", None)

use_bind = bind_env if bind_env else f"{host}:{port}"

workers_per_core_str = os.getenv("WORKERS_PER_CORE", "1")
max_workers_str = os.getenv("MAX_WORKERS")
web_concurrency_str = os.getenv("WEB_CONCURRENCY", None)

cores = multiprocessing.cpu_count()
workers_per_core = int(workers_per_core_str)
default_web_concurrency = workers_per_core * cores + 1

if web_concurrency_str:
    web_concurrency = int(web_concurrency_str)
    assert web_concurrency > 0
else:
    web_concurrency = max(int(default_web_concurrency), 2)
    if max_workers_str:
        use_max_workers = int(max_workers_str)
        web_concurrency = min(web_concurrency, use_max_workers)

graceful_timeout_str = os.getenv("GRACEFUL_TIMEOUT", "120")
timeout_str = os.getenv("TIMEOUT", "120")
keepalive_str = os.getenv("KEEP_ALIVE", "5")
use_loglevel = os.getenv("LOG_LEVEL", "info")

# Gunicorn config variables
loglevel = use_loglevel
workers = web_concurrency
bind = use_bind
worker_tmp_dir = "/dev/shm"
graceful_timeout = int(graceful_timeout_str)
timeout = int(timeout_str)
keepalive = int(keepalive_str)
logconfig = os.getenv("LOG_CONFIG", "/src/logging_production.ini")
