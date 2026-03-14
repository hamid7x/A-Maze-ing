CONFIG	= config.txt
MAIN	= a_maze_ing.py


build:
	python3 -m build --no-isolation

install:
	pip install --user virtualenv
	python3 -m virtualenv venv  
	venv/bin/pip install dist/mazegen-1.0.0-py3-none-any.whl
	venv/bin/pip install flake8 mypy

run:
	venv/bin/python $(MAIN) $(CONFIG)

debug:
	venv/bin/python -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	find . -type f -name "*.pyc" -exec rm -f {} +

clean-venv:
	rm -rf venv
lint:
	venv/bin/flake8 .
	venv/bin/mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	venv/bin/flake8 .
	venv/bin/mypy . --strict

.PHONY: build install run debug clean clean-venv lint lint-strict