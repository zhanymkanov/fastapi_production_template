default:
  just --list

up:
  docker-compose up -d

kill:
  docker-compose kill

ps:
  docker-compose ps

exec *args:
  docker-compose exec app {{args}}

mm *args:
  docker compose exec app alembic revision --autogenerate -m "{{args}}"

migrate:
  docker compose exec app alembic upgrade head

downgrade *args:
  docker compose exec app alembic downgrade {{args}}

ruff *args:
  docker compose exec app ruff {{args}} src

black:
  docker compose exec app black src

lint:
  just black
  just ruff --fix