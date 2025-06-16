PYTHON := python

ifeq (, $(shell which $(PYTHON)))
	PYTHON := python3
endif

.PHONY: help
help:
	@echo "Makefile commands:"
	@echo "  make install     - Install Python dependencies"
	@echo "  make run         - Run main.py"
	@echo "  make test        - Run tests"
	@echo "  make lint        - Lint code with flake8"
	@echo "  make format      - Format code with black"
	@echo "  make clean       - Remove __pycache__ and .pyc files"


install:
	$(PYTHON) -m pip install -r requirements.txt

run:
	$(PYTHON) main.py

test:
	$(PYTHON) -m unittest discover -s tests

lint:
	$(PYTHON) -m flake8 .

format:
	$(PYTHON) -m black .

clean:
	find . -type d -name '__pycache__' -exec rm -r {} + ; \
	find . -name '*.pyc' -delete