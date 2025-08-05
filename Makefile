test:
	PYTHONPATH=. pytest

lint:
	ruff check app tests --fix
	mypy

format:
	ruff format

build:
	podman build -t notes-backend .

run-image:
	podman run -d -p 8000:8000 notes-backend