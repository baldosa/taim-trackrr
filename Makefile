ENV_FILE ?= .env
VENV ?= .venv
BIN := $(VENV)/bin
SHELL := /bin/bash

GREEN=\033[0;32m
YELLOW=\033[0;33m
NOFORMAT=\033[0m

# Add env variables if needed
ifneq (,$(wildcard ${ENV_FILE}))
	include ${ENV_FILE}
    export
endif

default: help

.PHONY: help
#❓ help: @ Displays this message
help: SHELL := /bin/sh
help:
	@echo ""
	@echo "List of available MAKE targets for development usage."
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@grep -E '[a-zA-Z\.\-]+:.*?@ .*$$' $(firstword $(MAKEFILE_LIST))| tr -d '#'  | awk 'BEGIN {FS = ":.*?@ "}; {printf "${GREEN}%-30s${NOFORMAT} %s\n", $$1, $$2}'
	@echo ""

#💻 lint: @ Runs the black code formatter
.PHONY: lint
lint:
	$(BIN)/black --fast .

# setup: @ Setup requirements, db and third party apps
.PHONY: setup
setup: venv venv.activate install db db.seeds

#⚙️ venv: @  Create and a virtual env
.PHONY: venv
venv:
	python -m venv $(VENV)

#⚙️ venv.activate: @  Make active virtual environment
venv.activate:
	source $(VENV)/bin/activate

.PHONY: install
#📦 setup: @ Install requirements
install:
	@$(BIN)/pip3 install -r requirements.txt

#💻 db: @ Create db
db:
	@$(BIN)/alembic upgrade head

#💻 db.seeds: @ Run seeds
db.seeds:
	@$(BIN)/python3 seeds.py