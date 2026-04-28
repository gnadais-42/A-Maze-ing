PYTHON		= python3
MAIN		= a_maze_ing.py
VENV		= venv
PIP		= $(VENV)/bin/pip
VENV_PYTHON	= $(VENV)/bin/python3

$(VENV):
	$(PYTHON) -m venv $(VENV)

install: .install

.install: $(VENV)
	$(PIP) install -r requirements/requirements.txt
	$(PIP) install requirements/mlx-2.2-py3-none-any.whl
	touch .install

run: $(VENV) install
	$(VENV_PYTHON) $(MAIN) config.txt

debug: $(VENV) install
	$(VENV_PYTHON) -m pdb $(MAIN) config.txt

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf $(VENV)
	rm -f .install

fclean: clean
	rm -rf dist
	rm -rf mazegen*egg*

build: $(VENV)
	$(PIP) install --quiet --upgrade build
	$(VENV_PYTHON) -m build

lint: $(VENV) install
	$(VENV)/bin/flake8 . --exclude=$(VENV)
	$(VENV)/bin/mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict: $(VENV) install
	$(VENV)/bin/flake8 . --exclude=$(VENV)
	$(VENV)/bin/mypy . --strict
	
.PHONY: install run debug clean lint lint-strict

