# This file is part of rss-reader
# https://github.com/scorphus/rss-reader

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2023, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# list all available targets
list:
	@sh -c "$(MAKE) -p no_targets__ | awk -F':' '/^[a-zA-Z0-9][^\$$#\/\\t=]*:([^=]|$$)/ {split(\$$1,A,/ /);for(i in A)print A[i]}' | grep -v '__\$$' | grep -v 'make\[1\]' | grep -v 'Makefile' | sort"
.PHONY: list
# required for list
no_targets__:

# install dependencies and pre-commit hooks
setup:
	@PIP_REQUIRE_VIRTUALENV=true pip install -U -e .\[tests,mypy\]
	@pre-commit install -f --hook-type pre-commit
	@pre-commit install -f --hook-type pre-push
.PHONY: setup

# install dependencies
setup-ci:
	@pip install -U -e .\[tests,mypy\]
.PHONY: setup-ci

# spin up a postgres container
db:
	@docker stop test_postgres || true
	@docker rm test_postgres || true
	@docker run --name test_postgres -p 5432:5432 \
		-e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=rss_reader \
		-d postgres
.PHONY: db

# create all tables in database
create-tables:
	@rss-reader create-tables
.PHONY: create-tables

# drop all tables from database
drop-tables:
	@rss-reader drop-tables
.PHONY: drop-tables

# drop and create all tables in database
db-reset: drop-tables create-tables
.PHONY: db-reset

# run the API with debug level logging
run:
	@uvicorn rss_reader.api:app --reload --log-level debug

# run isort, black and pylint for style guide enforcement
isort:
	@isort .
.PHONY: isort

black:
	@black .
.PHONY: black

pylint:
	@pylint rss_reader tests
.PHONY: pylint

mypy:
	@mypy .
	@echo Remember to run “make mypy-strict” for strict type checking
.PHONY: mypy

mypy-strict:
	@mypy --strict .
.PHONY: mypy-strict

lint: isort black pylint mypy
.PHONY: lint

# spin up a postgres container for testing
test-db:
	@docker stop test_postgres || true
	@docker rm test_postgres || true
	@docker run --name test_postgres -p 5434:5432 \
		-e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=rss_reader_test \
		-d postgres
.PHONY: test-db

# run tests with coverage
test:
	@pytest --cov=rss_reader tests
.PHONY: test

# report coverage in html format
coverage: test
	@coverage html
.PHONY: coverage
