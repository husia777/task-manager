env:
	cp config/.env.template config/.env

install-local:
	poetry install && poetry run pre-commit install


format-lint:
	poetry run pre-commit run --all-files

check:
	@poetry run ruff check && \
	poetry run ruff format --check && \
	poetry run mypy . && \
	echo ""

build-dev:
	docker compose build

up-dev:
	docker compose up -d


down:
	docker compose down --remove-orphans


makemigration:
	@LOG_LEVEL=info PYTHONPATH=. poetry run  alembic --config "./alembic.ini" revision --autogenerate

migrate:
	@LOG_LEVEL=info poetry run alembic --config "alembic.ini" upgrade head

upgrade:
	@LOG_LEVEL=info poetry run alembic --config "alembic.ini" upgrade +1

downgrade:
	@LOG_LEVEL=info poetry run alembic --config "alembic.ini" downgrade -1
