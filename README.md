# FastAPI Example Project
A lot of people after reading my previous article on [FastAPI best practices](https://github.com/zhanymkanov/fastapi-best-practices)
were searching my profile for project examples based on that conventions. 
Unfortunately, I didn't have public repositories I could show, but only old proof of concept samples. 

This repo is kind of a template I use when starting up new FastAPI projects:
- production-ready Dockerfile
  - gunicorn with dynamic workers configuration (stolen from [@tiangolo](https://github.com/tiangolo)) and JSON logs
  - optimized for small size and fast builds
  - non-root user
- easy local development
  - environment with configured postgres and redis
  - script to lint code with `black`, `autoflake`, `isort`
  - configured pytest with `async-asgi-testclient`, `pytest-env`, `pytest-asyncio`
  - fully typed to comply with `mypy`
- SQLAlchemy with slightly configured `alembic`
  - async db calls with `asyncpg`
  - set up `sqlalchemy2-stubs`
  - migrations set in easy to sort format (`YYYY-MM-DD_slug`)
- pre-installed JWT authorization
  - short-lived access token
  - long-lived refresh token which lives in http-only cookies
  - salted password storage with `bcrypt`
- global pydantic model with 
  - `orjson`
  - explicit timezone setting during JSON export
- and some other extras like global exceptions, sqlalchemy keys naming convention, shortcut scripts for alembic, etc.

## Local Development

### First Build Only
1. `cp .env.example .env`
2. `docker network create app_main`
3. `docker-compose up -d --build`

### Linters
Format the code
```shell
docker compose exec app format
```

### Migrations
- Create an automatic migration from changes in `src/database.py`
```shell
docker compose exec app makemigrations *migration_name*
```
- Run migrations
```shell
docker compose exec app migrate
```
- Downgrade migrations
```shell
docker compose exec app downgrade -1  # or -2 or base or hash of the migration
```
### Tests
All tests are integrational and require DB connection. 

One of the choices I've made is to use default database (`postgres`), separated from app's `app` database.
- Using default database makes it easier to run tests in CI/CD environments, since there is no need to setup additional databases
- Tests are run with `force_rollbacke=True`, i.e. every transaction made is then reverted

Run tests
```shell
docker compose exec app pytest
```