import multiprocessing

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

try:
    from prometheus_client import multiprocess

    def child_exit(_, worker):
        multiprocess.mark_process_dead(worker.pid)

except ImportError:
    pass


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    host: str = "0.0.0.0"
    port: int = 8000
    bind: str | None = None

    workers_per_core: int = Field(1)
    max_workers: int | None = None
    web_concurrency: int | None = None

    graceful_timeout: int = 120
    timeout: int = 120
    keepalive: int = 5
    log_level: str = "INFO"
    log_config: str = "/src/logging_production.ini"

    @property
    def computed_bind(self) -> str:
        return self.bind if self.bind else f"{self.host}:{self.port}"

    @property
    def computed_web_concurrency(self) -> int:
        cores = multiprocessing.cpu_count()
        default_web_concurrency = self.workers_per_core * cores + 1

        if self.web_concurrency:
            assert self.web_concurrency > 0
            return self.web_concurrency
        else:
            web_concurrency = max(default_web_concurrency, 2)
            if self.max_workers:
                return min(web_concurrency, self.max_workers)

            return web_concurrency


settings = Settings()

# Gunicorn config variables
loglevel = settings.log_level
workers = settings.computed_web_concurrency
bind = settings.computed_bind
worker_tmp_dir = "/dev/shm"
graceful_timeout = settings.graceful_timeout
timeout = settings.timeout
keepalive = settings.keepalive
logconfig = settings.log_config
