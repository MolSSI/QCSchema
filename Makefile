.PHONY: install
install:
	pip install -e .

.PHONY: test
test:
	pytest -v

.PHONY: docs
docs:
	cd docs && make html
