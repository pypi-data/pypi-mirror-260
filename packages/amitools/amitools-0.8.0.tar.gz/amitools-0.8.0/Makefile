# Makefile for amitools

BUILD_DIR = build
DIST_DIR = dist

PYTHON ?= python3
PIP ?= $(PYTHON) -m pip

SHOW_CMD = open
#PYTHON = python-dbg

.PHONY: help init build test docker-tox docs show
.PHONY: clean clean_all clean_git clean_py
.PHONY: init sdist bdist upload

help:
	@echo "init        initialize project"
	@echo "build       build native extension"
	@echo
	@echo "format      format source code with black"
	@echo
	@echo "test        run tests"
	@echo "docker-build  build tox docker container"
	@echo
	@echo "docs        generate docs"
	@echo "show        show docs in browser"
	@echo
	@echo "clean       clean build"
	@echo "clean_all   clean dist"
	@echo "clean_git   clean non-git files"
	@echo "clean_py    remove compiled .pyc files"
	@echo "clean_ext   remove native extension build"
	@echo
	@echo "install     install package"
	@echo "sdist       build source dist"
	@echo "bdist       build bin dist wheel"
	@echo "upload      upload sdist with twine to pypi"

init:
	$(PIP) install --upgrade setuptools pip
	$(PIP) install --upgrade -r requirements-dev.txt
	$(PIP) install --upgrade -r requirements-test.txt
	$(PIP) install --upgrade --editable .

build:
	$(PYTHON) setup.py build_ext -i

format:
	black .

# testing
test:
	./local-tox

# doc
docs:
	[ -d build/docs/html ] || mkdir -p build/docs/html
	sphinx-build -b html docs build/docs/html

show:
	$(SHOW_CMD) build/docs/html/index.html

# clean
clean:
	rm -rf $(BUILD_DIR)

clean_all: clean clean_ext
	rm -rf $(DIST_DIR)

clean_git:
	git clean -fxd

clean_py:
	find . -name *.pyc -exec rm {} \;

clean_ext:
	$(PYTHON) setup.py clean

# install, distrib
install:
	$(PIP) install --upgrade --editable .

sdist:
	$(PYTHON) -m build -s

bdist:
	$(PYTHON) -m build -w

upload: sdist
	twine upload dist/*

# container
docker-build:
	docker build -t amitools-tox .
