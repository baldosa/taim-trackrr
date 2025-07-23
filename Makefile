ENV_FILE ?= .env
VENV ?= .venv
BIN := $(VENV)/bin

#⚙️ venv: @  Create and a virtual env
.PHONY: venv
venv:
	python -m venv $(VENV)

#⚙️  venv.activate: @  Make active venv environment
venv.activate:
	source $(VENV)/bin/activate

.PHONY: install
#📦 setup: @ Install requirements
install:
	@$(BIN)/pip3 install -r requirements.txt

#💻 db: @ Create db
db:
	@$(BIN)/ alembic upgrade head

#💻 db.seeds: @ Run seeds
db.seeds:
	@$(BIN)/python3 seeds.py