# ifeq ($(shell test -e '.env' && echo -n yes),yes)
# 	include .env
# endif

include .env

# Manually define main variables

ifndef APP_PORT
override APP_PORT = 8000
endif

ifndef APP_HOST
override APP_HOST = 127.0.0.1
endif

# parse additional args for commands

args := $(wordlist 2, 100, $(MAKECMDGOALS))
ifndef args
MESSAGE = "No such command (or you pass two or many targets to ). List of possible commands: make help"
else
MESSAGE = "Done"
endif

APPLICATION_NAME = src
APPLICATION_HOST = 0.0.0.0
APPLICATION_PORT = 8080
TEST = poetry run python -m pytest --verbosity=2 --showlocals --log-level=DEBUG
CODE = $(APPLICATION_NAME) tests

HELP_FUN = \
	%help; while(<>){push@{$$help{$$2//'options'}},[$$1,$$3] \
	if/^([\w-_]+)\s*:.*\#\#(?:@(\w+))?\s(.*)$$/}; \
    print"$$_:\n", map"  $$_->[0]".(" "x(20-length($$_->[0])))."$$_->[1]\n",\
    @{$$help{$$_}},"\n" for keys %help; \

# Commands
env:  ##@Environment Create .env file with variables
	@cp .env.example .env

env-win:  ##@Environment Create .env file with variables (for Windows)
	copy .\.env.example .\.env

help: ##@Help Show this help
	@echo -e "Usage: make [target] ...\n"
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)

db:  ##@Database Create database with docker-compose
	docker compose -f docker-compose.yml up -d --remove-orphans postgres

lint:  ##@Code Check code with pylint
	poetry run python -m ruff check $(CODE) --fix

format:  ##@Code Reformat code with isort and black
	poetry run python3 -m isort $(CODE)
	poetry run python3 -m black $(CODE)

migrate:  ##@Database Do all migrations in database
	cd $(APPLICATION_NAME)/db && poetry run alembic upgrade $(args)

run-locally:  ##@Application Run application server
	poetry run python3 -m $(APPLICATION_NAME)

run:
	poetry run uvicorn $(APPLICATION_NAME).__main__:app --host $(APP_HOST) --port $(APP_PORT)

setup:  ##@Application Create database and with docker-compose
	docker compose -f docker-compose.yml up -d --remove-orphans --build postgres backend nginx

revision:  ##@Database Create new revision file automatically with prefix (ex. 2022_01_01_14cs34f_message.py)
	cd $(APPLICATION_NAME)/db && poetry run alembic revision --autogenerate

test:  ##@Testing Test application with pytest
	$(TEST)

test-cov:  ##@Testing Test application with pytest and create coverage report
	make db && $(TEST) --cov=$(APPLICATION_NAME) --cov-report html --cov-fail-under=70

clean:  ##@Code Clean directory from garbage files
	rm -fr *.egg-info dist

psql:
	docker exec -it postgres psql -d belot_db -h localhost -U user

build:
	docker compose -f docker-compose.yml up -d --remove-orphans

%::
	echo $(MESSAGE)

.PHONY: frontend-clean frontend-deploy frontend-setup

frontend-clean:
	@echo "🧹 Cleaning old frontend distribution files..."
	@if [ -d "nginx/dist" ]; then rm -rf nginx/dist; echo "✅ nginx/dist removed"; else echo "ℹ️ nginx/dist not found"; fi

frontend-deploy:
	@echo "🚀 Deploying new frontend distribution..."
	@if [ ! -d "nginx/dist" ]; then \
		echo "❌ nginx/dist directory not found. Please upload dist folder first."; \
		exit 1; \
	fi
	@echo "✅ Frontend distribution deployed successfully!"

frontend-setup: frontend-clean frontend-deploy
	@echo "ℹ️ frontend-setup completed"
