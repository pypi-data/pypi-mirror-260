# Variables
PYTHON = python3
PIP = pip
TEST_DIR = tests
SRC_DIR = src
COVERAGE_DIR = coverage
PYLINT_DIR = pylint

# Targets
.PHONY: install format pylint build test coverage push

help:
	@echo "Available targets:"
	@echo "  install    - Install the project"
	@echo "  format     - Format the code"
	@echo "  pylint     - Run pylint and generate HTML report"
	@echo "  mypy	    - Run mypy"
	@echo "  setup      - Install dependencies"
	@echo "  build      - Build the project"
	@echo "  test       - Run tests"
	@echo "  coverage   - Generate coverage report"
	@echo "  push       - Push changes to the repository"

install:
	$(PIP) install -e .

format:
	$(PYTHON) -m autopep8 --in-place --recursive .

pylint:
	$(PYTHON) -m pylint $(SRC_DIR) --output-format=json2 --reports y > pylint.json
	$(PYTHON) -m pylint_json2html pylint.json  -o pylint.html

mypy:
	$(PYTHON) -m mypy --ignore-missing-imports $(SRC_DIR)

autopep8:
	$(PYTHON) -m autopep8 --in-place --recursive .

setup:
	$(PYTHON) -m $(PIP) install --upgrade pip
	$(PYTHON) -m $(PIP) install -r requirements.txt

build: setup format pylint

test:
	$(PYTHON) -m pytest --cov=$(SRC_DIR) $(TEST_DIR)

coverage:
	$(PYTHON) -m coverage report -m

push:
	git add .
	git commit -m "Update"
	git push

clean:
	rm -rf $(COVERAGE_DIR) $(PYLINT_DIR) pylint.json
	rm -rf dist
	rm -rf htmlcov
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .coverage*
	rm -rf *.egg-info

publish:
	$(PYTHON) -m build
	$(PYTHON) -m twine upload dist/*