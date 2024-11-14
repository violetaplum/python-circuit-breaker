.PHONY: setup test run clean docker-build docker-run

setup:
	python -m venv venv
	. venv/bin/activate && pip install -r requirements.txt

test:
	python -m pytest tests/

run:
	python src/example.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete

docker-build:
	docker-compose build

docker-run:
	docker-compose up
