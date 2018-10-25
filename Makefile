INTEGRATION_DIR = test/integration
UNIT_DIR = test/unit
CONTAINER_NAME = utt-integration-py$*
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
	pipenv run yapf --in-place --recursive *.py utt test

.PHONY: bdist_wheel
bdist_wheel:
	pipenv run python setup.py bdist_wheel --universal

.PHONY: lint
lint:
	pipenv run pylint utt test

.PHONY: sdist
sdist:
	pipenv run python setup.py sdist

.PHONY: test
test: test-unit test-integration

.PHONY: test-integration
test-integration: clean test-integration-py2 test-integration-py3

.PHONY: test-integration-py%
test-integration-py%: test-integration-container-py%
	docker run --rm -ti -v "$(CURDIR)/$(INTEGRATION_DIR):/utt:ro" $(CONTAINER_NAME) $(INTEGRATION_CMD)

.PHONY: test-integration-container-py%
test-integration-container-py%: $(INTEGRATION_DIR)/utt-$(VERSION).tar.gz $(INTEGRATION_DIR)/utt-$(VERSION)-py2.py3-none-any.whl
	docker build -t $(CONTAINER_NAME) -f $(INTEGRATION_DIR)/Dockerfile.py$* $(INTEGRATION_DIR)

.PHONY: test-unit
test-unit:
	pipenv run pytest --verbose --cov=utt test/unit

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
