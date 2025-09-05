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

check-fix:
	@poetry run ruff check --fix \

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


run-in-kubernetes:
	kubectl apply -f ./kubernetes/app-config.yaml
	kubectl apply -f ./kubernetes/app-secrets.yaml
	kubectl apply -f ./kubernetes/postgres-service.yaml
	kubectl apply -f ./kubernetes/postgres-statefulset.yaml
	kubectl wait --for=condition=ready pod -l app=postgres --timeout=120s
	kubectl apply -f ./kubernetes/api-migrations.yaml
	kubectl wait --for=condition=complete job/alembic-migration --timeout=120s
	kubectl apply -f ./kubernetes/api-service.yaml
	kubectl apply -f ./kubernetes/api-deployment.yaml


clear-default-ns:
	kubectl scale deployment api-deployment --replicas=0 -n default
	kubectl delete statefulset postgres -n default --force --grace-period=0
	kubectl delete pods --all --grace-period=0 --force -n default
	kubectl delete -f ./kubernetes/app-config.yaml -n default
	kubectl delete -f ./kubernetes/app-secrets.yaml -n default
	kubectl delete -f ./kubernetes/postgres-service.yaml -n default
	kubectl delete -f ./kubernetes/api-migrations.yaml -n default
	kubectl delete -f ./kubernetes/api-service.yaml -n default
	kubectl delete -f ./kubernetes/api-deployment.yaml -n default
	kubectl delete pvc postgres-storage-postgres-0

check-default-ns:
	@echo "=== Default Namespace ==="
	kubectl get pods -n default
	@echo ""
