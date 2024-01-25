PYTHON := python3.12
VENV_DIR := .venv
VENV_PYTHON := $(VENV_DIR)/bin/python

SERVICE_NAME := delivery-fee-calculator-api
DOCKER_EXEC = docker compose exec $(SERVICE_NAME)

INIT_VENV := $(VENV_DIR)/init_venv_stamp
.PHONY: init-venv
init-venv: $(INIT_VENV)
$(INIT_VENV): requirements.txt requirements-dev.txt
		$(PYTHON) -m venv $(VENV_DIR)
		$(VENV_PYTHON) -m pip install --upgrade pip
		$(VENV_PYTHON) -m pip install -r requirements.txt
		$(VENV_PYTHON) -m pip install -r requirements-dev.txt
		touch $@


DOCKER_BUILD := tmp/docker_build_stamp
.PHONY: docker-build
docker-build: $(DOCKER_BUILD)
$(DOCKER_BUILD): Dockerfile requirements.txt requirements-dev.txt
	docker-compose build $(SERVICE_NAME)
	mkdir -p tmp
	touch $@


.PHONY: docker-up-d
docker-up-d: docker-build
	docker compose up $(SERVICE_NAME) -d


.PHONY: run-dev
run-dev: docker-up-d
	docker compose logs -f $(SERVICE_NAME)


.PHONY: test
test: docker-up-d
	$(DOCKER_EXEC) pytest -v


.PHONY: test-watch
test-watch: docker-up-d
	$(DOCKER_EXEC) ptw -- --continue-on-collection-errors -v


.PHONY: test-coverage
test-coverage: docker-up-d
	$(DOCKER_EXEC) pytest --cov=app --cov-report=term-missing --cov-report=html


.PHONY: format
format: docker-up-d
	${DOCKER_EXEC} black .


.PHONY: lint
lint: docker-up-d
	${DOCKER_EXEC} ruff check .


.PHONY: lint-fix
lint-fix: docker-up-d
	${DOCKER_EXEC} ruff check . --fix


.PHONY: type-check
type-check: docker-up-d
	${DOCKER_EXEC} mypy app


.PHONY: docs
docs: docker-up-d
	@while ! curl -s http://localhost:8000/docs > /dev/null; do sleep 1; done
	open http://localhost:8000/docs


.PHONY: docker-down
docker-down:
	- docker compose down


.PHONY: clean-docker
clean-docker: docker-down
	-docker image rm $(SERVICE_NAME)
	rm -rf $(DOCKER_BUILD)


.PHONY: clean-all
clean-all: clean-docker
	rm -rf $(VENV_DIR)
	rm -rf tmp
	rm -rf htmlcov
	rm -rf app/__pycache__
	rm -rf tests/__pycache__