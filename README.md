# FastAPI Example Project
Some people were searching my GitHub profile for project examples after reading the article on [FastAPI best practices](https://github.com/zhanymkanov/fastapi-best-practices).
Unfortunately, I didn't have useful public repositories, but only my old proof-of-concept projects. 

Hence, I have decided to fix that and show how I start projects nowadays, after getting some real-world experience. 
This repo is kind of a template I use when starting up new FastAPI projects:
- production-ready
  - gunicorn with dynamic workers configuration (stolen from [@tiangolo](https://github.com/tiangolo))
  - Dockerfile optimized for small size and fast builds with a non-root user
  - JSON logs
  - sentry for deployed envs
- easy local development
  - environment with configured postgres and redis
  - script to lint code with `black`, `autoflake`, `isort` (also stolen from [@tiangolo](https://github.com/tiangolo))
  - configured pytest with `async-asgi-testclient`, `pytest-env`, `pytest-asyncio`
  - fully typed to comply with `mypy`
- SQLAlchemy with slightly configured `alembic`
  - async db calls with `asyncpg`
  - set up `sqlalchemy2-stubs`
  - migrations set in easy to sort format (`YYYY-MM-DD_slug`)
- pre-installed JWT authorization
  - short-lived access token
  - long-lived refresh token which is stored in http-only cookies
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
- Tests are run with `force_rollback=True`, i.e. every transaction made is then reverted

Run tests
```shell
docker compose exec app pytest
```
