.PHONY: build lint test

build: lint test
	poetry build

lint:
	black --check scru160 tests
	mypy --strict scru160 tests

test:
	python -m unittest -v
