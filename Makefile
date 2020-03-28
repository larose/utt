INTEGRATION_DIR = test/integration
UNIT_DIR = test/unit
CONTAINER_NAME = utt-integration-py$*
SOURCE_DIRECTORIES=utt test
VERSION := $(shell python3 setup.py --version)

.PHONY: all
all:

.PHONY: clean
clean:
	rm -rf build
	rm -rf dist
	rm -f $(INTEGRATION_DIR)/utt-*.tar.gz
	rm -f $(INTEGRATION_DIR)/utt-*.whl

.PHONY: format
format:
	pipenv run black utt test
	pipenv run isort --recursive $(SOURCE_DIRECTORIES)

.PHONY: bdist_wheel
bdist_wheel:
	pipenv run python setup.py bdist_wheel --universal

.PHONY: install-dev
install-dev:
	pipenv install --dev --deploy

.PHONY: lint
lint:
	pipenv run flake8 utt test
	pipenv run isort --check-only --diff --ignore-whitespace --recursive --quiet $(SOURCE_DIRECTORIES)
	pipenv run black --diff --check $(SOURCE_DIRECTORIES)

.PHONY: sdist
sdist:
	pipenv run python setup.py sdist

.PHONY: test
test: test-unit test-integration

.PHONY: test-integration
test-integration: clean test-integration-container
	docker run --rm -ti --mount source=utt-pip-cache,target=/root/.cache/pip $(CONTAINER_NAME) $(INTEGRATION_CMD)

.PHONY: test-integration-container
test-integration-container: $(INTEGRATION_DIR)/utt-$(VERSION).tar.gz $(INTEGRATION_DIR)/utt-$(VERSION)-py2.py3-none-any.whl
	docker build -t $(CONTAINER_NAME) $(INTEGRATION_DIR)

.PHONY: test-unit
test-unit:
	pipenv run pytest --verbose --verbose test/unit

.PHONY: upload
upload: clean test-unit test-integration
	pipenv run twine upload --username mathieularose dist/*

.PHONY: upload-test
upload-test: clean test-unit test-integration
	pipenv run twine upload --username mathieularose --repository-url https://test.pypi.org/legacy/ dist/*

$(INTEGRATION_DIR)/utt-$(VERSION).tar.gz: sdist
	cp dist/utt-$(VERSION).tar.gz $@

$(INTEGRATION_DIR)/utt-$(VERSION)-py2.py3-none-any.whl: bdist_wheel
	cp dist/utt-$(VERSION)-py2.py3-none-any.whl $@
