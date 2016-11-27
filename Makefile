# System binaries
SYSTEM_PIP=$(shell which pip3)
SYSTEM_PYTHON=$(shell which python3)
SYSTEM_VIRTUALENV=$(shell which virtualenv)

# Project binaries
PYTHON=$(ENV_DIR)/bin/python3
PYLINT=$(ENV_DIR)/bin/pylint
PIP=$(ENV_DIR)/bin/pip3
COVERAGE_PY=$(ENV_DIR)/bin/coverage

# Directories
LIB_DIR=./lib
TEST_DIR=./test
SRC_DIR=./src
ENV_DIR=$(LIB_DIR)/env

# Flags
TEST_FILES=test_*.py
REQUIREMENTS=$(LIB_DIR)/requirements.txt
PYLINT_CONFIG=$(TEST_DIR)/pylint.rc
MODULES=$(SRC_DIR):$(TEST_DIR)

# Environment variables
export PYTHONPATH=$(MODULES)
export PYTHONDONTWRITEBYTECODE=true

install: pip-install
test: unit-test
lint: pylint
coverage: coverage-py

virtualenv-install:
	$(SYSTEM_PIP) install virtualenv
	$(SYSTEM_VIRTUALENV) -p $(SYSTEM_PYTHON) --no-site-packages $(ENV_DIR)

pip-install: virtualenv-install
	@$(PIP) install -r $(REQUIREMENTS)

unit-test:
	@$(PYTHON) -m unittest discover -s $(TEST_DIR) -p $(TEST_FILES)

pylint:
	@$(PYTHON) $(PYLINT) --rcfile $(PYLINT_CONFIG) $(SRC_DIR)/* $(TEST_DIR)

coverage-py:
	@$(COVERAGE_PY) run --source=$(SRC_DIR) -m unittest discover -s $(TEST_DIR) -p $(TEST_FILES)

.PHONY: install test lint
