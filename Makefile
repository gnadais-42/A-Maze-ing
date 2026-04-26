PYTHON		= python3
MAIN		= main.py
VENV		= venv
PIP		= $(VENV)/bin/pip
VENV_PYTHON	= $(VENV)/bin/python

$(VENV):
	$(PYTHON) -m venv $(VENV)

install: .install

.install: $(VENV)
	$(PIP) install -r requirements/requirements.txt
	$(PIP) install requirements/mlx-2.2-py3-none-any.whl
	touch .install

run: $(VENV) install
	$(VENV_PYTHON) $(MAIN)

debug: $(VENV) install
	$(VENV_PYTHON) -m pdb $(MAIN)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm .install
	rm -rf $(VENV)

lint: $(VENV)
	$(VENV)/bin/flake8 .
	$(VENV)/bin/mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict: $(VENV)
	$(VENV)/bin/flake8 .
	$(VENV)/bin/mypy . --strict
	
.PHONY: install run debug clean lint lint-strict

