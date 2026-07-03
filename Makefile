.PHONY: venv test run lint clean

venv:
	python3 -m venv .venv
	.venv/bin/pip install pytest

test: venv
	.venv/bin/python -m pytest tests/ -v

run: venv
	.venv/bin/python server.py

lint:
	.venv/bin/ruff check .

clean:
	rm -rf .venv __pycache__ .pytest_cache
