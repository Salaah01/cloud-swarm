VENV = venv
PYTHON = ${VENV}/bin/python3
PIP = ${VENV}/bin/pip3

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(notdir $(patsubst %/,%,$(dir $(mkfile_path))))
current_dir_full_path := $(abspath $(current_dir))

# -----------------------------------------------------------------------------
# LOCAL USAGE

# Creates a virtual environment for the project.
venv:
	python3 -m venv venv

# Intall dependencies.
install: venv site/requirements.txt
	${PIP} install -r site/requirements.txt

# Runs migrations and the server.
runserver: install
	${PYTHON} site/manage.py migrate
	${PYTHON} site/manage.py runserver


# Runs the tests locally.
test: install
	${PYTHON} site/manage.py test

# Runs linter
lint: install
	${PYTHON} -m flake8 site/
