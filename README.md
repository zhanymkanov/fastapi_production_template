# FastAPI Template
This repo is kind of a template I use when starting up new FastAPI projects:
- easy local development
  - environment with configured postgres
  - script to lint code with `ruff` and `ruff format`
- SQLAlchemy with slightly configured `alembic`
  - async SQLAlchemy engine
  - pessimistic connection pooling configuration ([link](https://docs.sqlalchemy.org/en/20/core/pooling.html#module-sqlalchemy.pool))
  - migrations set in easy to sort format (`YYYY-MM-DD_slug`)
  - migrations are formated with `ruff`
- global pydantic model with 
  - explicit timezone setting during JSON export
- some configs for production
  - gunicorn with dynamic workers configuration (stolen from [@tiangolo](https://github.com/tiangolo))
  - Dockerfile optimized for small size and fast builds with a non-root user
  - JSON logs
  - sentry for deployed envs
- and some other extras like global exceptions, sqlalchemy keys naming convention, shortcut scripts for alembic, etc.

## Local Development

### Setup just
MacOS:
```shell
brew install just
```

Debian/Ubuntu:
```shell
apt install just
````

Others: [link](https://github.com/casey/just?tab=readme-ov-file#packages)

### Setup poetry
```shell
pip install poetry
```

Other ways: [link](https://python-poetry.org/docs/#installation)

### Setup Postgres (16.3)
```shell
just up
```
### Copy the environment file and install dependencies
1. `cp .env.example .env`
2. `poetry install`

### Run the uvicorn server
With default settings:
```shell
just run
```
With extra configs (e.g. logging file)
```shell
just run --log-config logging.ini
```

### Linters
Format the code with `ruff --fix` and `ruff format`
```shell
just lint
```

### Migrations
- Create an automatic migration from changes in `src/database.py`
```shell
just mm *migration_name*
```
- Run migrations
```shell
just migrate
```
- Downgrade migrations
```shell
just downgrade downgrade -1  # or -2 or base or hash of the migration
```

## Deployment
Deployment is done with Docker and Gunicorn. The Dockerfile is optimized for small size and fast builds with a non-root user. The gunicorn configuration is set to use the number of workers based on the number of CPU cores.

Example of running the app with docker compose:
```shell
docker compose -f docker-compose.prod.yml up -d --build
```