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
SRC_DIR=./src
LIB_DIR=./lib
TEST_DIR=./test
DIST_DIR=./dist
ENV_DIR=$(LIB_DIR)/env

# Flags
TEST_FILES=test_*.py
REQUIREMENTS=$(LIB_DIR)/requirements.txt
PYLINT_CONFIG=$(TEST_DIR)/pylint.rc
MODULES=$(SRC_DIR):$(TEST_DIR)

# Distribution
MAIN_FILE=$(SRC_DIR)/main.py
OUTFILE=$(DIST_DIR)/stenograpi.py
SOURCE_FILES=$(shell find src -name "*.py" -and -not -name "main.py")
IGNORE=grep -v 'from \.\|from incoming\|from stenograpi'

# Environment variables
export PYTHONPATH=$(MODULES)
export PYTHONWARNINGS=ignore
export PYTHONDONTWRITEBYTECODE=true

distribute: combine-to-one-script
install: pip-install
test: unit-test
lint: pylint
coverage: coverage-py

combine-to-one-script: $(SOURCE_FILES)
	-@[ -e $(OUTFILE) ] && rm $(OUTFILE);
	@for source_file in $(SOURCE_FILES) ; do \
		cat $$source_file  | $(IGNORE) >> $(OUTFILE) ; \
	done;
	@cat $(MAIN_FILE) | $(IGNORE) >> $(OUTFILE);

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
	@$(PYTHON) $(COVERAGE_PY) run --source=$(SRC_DIR) -m unittest discover -s $(TEST_DIR) -p $(TEST_FILES)

.PHONY: install test lint
