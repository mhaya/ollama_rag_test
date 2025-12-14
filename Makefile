PYTHON := $(shell which python3)
VENV := .venv
PIP := $(VENV)/bin/pip
RUN := $(VENV)/bin/python

.PHONY: deps serve ingest test lint format

deps:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install -U pip
	$(PIP) install -r requirements.txt

serve:
	$(RUN) -m uvicorn src.app:app --reload --host 0.0.0.0 --port 5000

ingest:
	$(RUN) src/ingest.py

test:
	$(RUN) -m pytest -q

lint:
	$(RUN) -m ruff check src tests

format:
	$(RUN) -m ruff format src tests
