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


########################################################################################
# TESTS
########################################################################################

.PHONY: tests
tests: unit-tests integration-tests functional-tests

unit-tests:
	poetry run pytest tests/unit

integration-tests:
	poetry run pytest tests/integration

functional-tests:
	poetry run pytest -W ignore::DeprecationWarning tests/functional

migrations-tests:
	poetry run pytest tests/migrations

cov-tests:
	rm -rf .coverage cov_html coverage.xml \
	&& poetry run pytest -x --cov-report html:cov_html tests/unit \
	&& poetry run pytest -x --cov-report html:cov_html -W ignore::DeprecationWarning tests/integration \
	&& poetry run pytest -x --cov-report html:cov_html tests/functional
