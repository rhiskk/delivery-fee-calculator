PYTHON := python3.12
VENV_DIR := .venv
VENV_PYTHON := $(VENV_DIR)/bin/python

DOCKER_EXEC = docker compose exec delivery-fee-calculator-api

INIT_VENV := $(VENV_DIR)/init_venv_stamp
.PHONY: init-venv
init-venv: $(INIT_VENV)
$(INIT_VENV): requirements.txt dev-requirements.txt
		$(PYTHON) -m venv $(VENV_DIR)
		$(VENV_PYTHON) -m pip install --upgrade pip
		$(VENV_PYTHON) -m pip install -r requirements.txt
		$(VENV_PYTHON) -m pip install -r dev-requirements.txt
		touch $@


DOCKER_BUILD := tmp/docker_build_stamp
.PHONY: docker-build
docker-build: $(DOCKER_BUILD)
$(DOCKER_BUILD): Dockerfile
	docker-compose build delivery-fee-calculator-api
	mkdir -p tmp
	touch $@


.PHONY: run-dev
run-dev: docker-build
	docker compose up delivery-fee-calculator-api


.PHONY: docker-up-d
docker-up-d: docker-build
	docker compose up -d


.PHONY: test
test: docker-up-d
	$(DOCKER_EXEC) pytest -v


.PHONY: test-watch
test-watch: docker-up-d
	$(DOCKER_EXEC) ptw -- --continue-on-collection-errors -v


.PHONY: test-coverage
test-coverage: docker-up-d
	$(DOCKER_EXEC) pytest --cov=app --cov-report=term-missing --cov-report=html


.PHONY: lint
lint: docker-up-d
	${DOCKER_EXEC} ruff check app


.PHONY: lint-fix
lint-fix: docker-up-d
	${DOCKER_EXEC} ruff check app --fix


.PHONY: type-check
type-check: docker-up-d
	${DOCKER_EXEC} mypy app


.PHONY: docs
docs: docker-up-d
	@while ! curl -s http://localhost:8000/docs > /dev/null; do sleep 1; done
	open http://localhost:8000/docs


.PHONY: docker-down
docker-down:
	docker compose down


.PHONY: docker-clean
docker-clean: docker-down
	docker image rm delivery-fee-calculator-api