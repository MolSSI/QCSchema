.DEFAULT_GOAL := all
isort = isort -rc qcschema
black = black qcschema
autoflake = autoflake -ir --remove-all-unused-imports --ignore-init-module-imports --remove-unused-variables qcschema

.PHONY: install
install:
	pip install -e .

.PHONY: format
format:
	$(autoflake)
	$(isort)
	$(black)

.PHONY: lint
lint:
	$(isort) --check-only
	$(black) --check

.PHONY: install
install:
	pip install -e .

.PHONY: test
test:
	pytest -v

.PHONY: docs
docs:
	cd docs && make html
