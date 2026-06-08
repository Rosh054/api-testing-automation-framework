.PHONY: up down test test-docker coverage report logs reset install wait-api

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f

reset:
	docker compose down -v
	docker compose up -d --build

install:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt && pip install -r sample_api/requirements.txt

wait-api:
	@echo "Waiting for API to become ready..."
	@for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do \
		curl -sf http://localhost:8000/ready >/dev/null && echo "API is ready" && exit 0; \
		sleep 2; \
	done; \
	echo "API did not become ready in time"; exit 1

test: wait-api
	. .venv/bin/activate && pytest tests/ -v

test-docker: wait-api
	docker run --rm --network host -v "$(CURDIR)":/workspace -w /workspace \
		-e BASE_URL=http://localhost:8000 \
		-e DATABASE_URL=postgresql://apiuser:apipass@localhost:5432/api_test_db \
		python:3.11-slim bash -c "pip install -q -r requirements.txt && pytest tests/ -v"

coverage: wait-api
	. .venv/bin/activate && pytest tests/ --cov=tests --cov-report=term-missing --cov-report=html:reports/coverage

report: wait-api
	. .venv/bin/activate && pytest tests/ -v --html=reports/report.html --self-contained-html
