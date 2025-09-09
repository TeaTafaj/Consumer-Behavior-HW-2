.PHONY: install lint test run all clean

# install all dependencies
install:
	pip install -r requirements.txt

# check code style with flake8 (or pylint if you prefer)
lint:
	flake8 Consumer_Behavior.py test_consumer_behavior.py

# run tests
test:
	python -m pytest -vv --cov=hello test_consumer_behavior.py

# run the main analysis
run:
	python Consumer_Behavior.py

# do everything: lint, test, run
all: lint test run

# clean up cache and generated files
clean:
	rm -rf __pycache__ .pytest_cache *.png



