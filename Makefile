.PHONY: install dev run lint format typecheck test docker-dev docker-prod docker-down-dev docker-down-prod

install:
	pip install --upgrade pip && pip install .

dev:
	pip install --upgrade pip && pip install ".[dev]"

run:
	uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

lint:
	ruff check src/ tests/

format:
	ruff format src/ tests/
	ruff check --fix src/ tests/

typecheck:
	mypy src/

test:
	pytest -v

docker-dev:
	docker compose -f deploy/docker-compose.dev.yml up --build -d

docker-prod:
	docker compose -f deploy/docker-compose.prod.yml up --build -d

docker-down-dev:
	docker compose -f deploy/docker-compose.dev.yml down

docker-down-prod:
	docker compose -f deploy/docker-compose.prod.yml down
