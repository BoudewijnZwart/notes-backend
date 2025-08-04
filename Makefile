test:
	PYTHONPATH=. pytest

lint:
	ruff check app tests --fix
	mypy

format:
	ruff format