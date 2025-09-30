.PHONY: install format lint test run clean

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt
	pip install black flake8 pytest

format:
	black .

lint:
	flake8 . --max-line-length=100 --per-file-ignores="test_consumer_behavior.py:F401"

test:
	pytest -q

run:
	python Consumer_Behavior.py

clean:
	@echo "Cleaning build artifacts and caches..."
	@rm -f ads_by_device.png || true
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true



