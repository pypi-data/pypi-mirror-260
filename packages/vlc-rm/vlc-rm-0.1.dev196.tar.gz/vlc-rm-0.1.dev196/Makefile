# Define the name of your Python package
PKG_NAME = python-vlc-rm


# Define variables
PYTHON := python
COVERAGE := coverage

# Define the list of commands to run when building and testing your package
.PHONY: all
all: build test

.PHONY: build
build:
	python setup.py sdist bdist_wheel

.PHONY: install
install:
	pip install -e ./

.PHONY: test 
test:	 	

all:
	pytest -s tests/

transmitter:
	pytest -s tests/test_transmitter.py

photodetector:
	pytest -s tests/test_photodetector.py

indoorenv:
	pytest -s tests/test_indoorenv.py

recursivemodel:
	pytest -s tests/test_recursivemodel.py

ser:
	pytest -s tests/test_ser.py

.PHONY: clean
clean:
	rm -rf dist/ build/ htmlcov/ $(PKG_NAME).egg-info/ __pycache__/ .pytest_cache/

.PHONY: coverage
coverage:
	coverage run -a --branch --source src/vlc_rm -m pytest tests --junit-xml=./test-results/tests-python.xml --verbose --durations=15

html:	
	coverage html
