CONFIG	= config.txt
MAIN	= a_maze_ing.py

build:
	poetry build

install: build
	pip install dist/*.whl
	pip install flake8 mypy

run:
	python3 $(MAIN) $(CONFIG)

debug:
	python3 -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	find . -type f -name "*.pyc" -exec rm -f {} +


lint:
	flake8 . --exclude test_env
	mypy . --exclude test_env --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs


.PHONY: build install run debug clean lint