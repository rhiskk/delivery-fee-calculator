PYTHON := python3.12
VENV_DIR := .venv
VENV_PYTHON := $(VENV_DIR)/bin/python

INIT_VENV := $(VENV_DIR)/init_venv_stamp
.PHONY: init-venv
init-venv: $(INIT_VENV)
$(INIT_VENV): requirements.txt dev-requirements.txt
		$(PYTHON) -m venv $(VENV_DIR)
		$(VENV_PYTHON) -m pip install --upgrade pip
		$(VENV_PYTHON) -m pip install -r requirements.txt
		$(VENV_PYTHON) -m pip install -r dev-requirements.txt
		touch $@


.PHONY: run
run: 
	trap 'docker compose down' EXIT; docker compose up delivery-fee-calculator-api


.PHONY: test
test: init-venv
	$(VENV_PYTHON) -m pytest -v


.PHONY: test-watch
test-watch: init-venv
	$(VENV_DIR)/bin/ptw -- --continue-on-collection-errors -v


.PHONY: test-coverage
test-coverage: init-venv
	$(VENV_PYTHON) -m pytest --cov=app --cov-report=term-missing --cov-report=html


.PHONY: lint
lint: init-venv
	$(VENV_PYTHON) -m ruff check app


.PHONY: type-check
type-check: init-venv
	$(VENV_PYTHON) -m mypy app


.PHONY: clean-venv
clean-venv:
	rm -rf $(VENV_DIR)
