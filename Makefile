INTEGRATION_DIR = test/integration
UNIT_DIR = test/unit
TMP = tmp
PY3_VENV = tmp/test-venv-py3
CONTAINER_NAME = utt-integration-py$*
VERSION := $(shell python3 setup.py --version)

.PHONY: all
all:

.PHONY: clean
clean:
	rm -rf $(TMP)
	rm -f $(INTEGRATION_DIR)/utt-*.tar.gz

.PHONY: format
format:
	pipenv run yapf utt test -ir

.PHONY: sdist
sdist:
	mkdir -p $(TMP)
	python3 setup.py sdist --dist-dir $(TMP)

.PHONY: test
test: test-unit test-integration

.PHONY: test-integration
test-integration: clean test-integration-py2 test-integration-py3

.PHONY: test-integration-py%
test-integration-py%: test-integration-container-py%
	docker run --rm -ti -v "$(CURDIR)/$(INTEGRATION_DIR):/utt:ro" $(CONTAINER_NAME) $(INTEGRATION_CMD)

.PHONY: test-integration-container-py%
test-integration-container-py%: $(INTEGRATION_DIR)/utt-$(VERSION).tar.gz
	docker build -t $(CONTAINER_NAME) -f $(INTEGRATION_DIR)/Dockerfile.py$* $(INTEGRATION_DIR)

.PHONY: test-unit
test-unit:
	python3 -m venv --clear $(PY3_VENV)
	$(PY3_VENV)/bin/pip3 install argcomplete pytz tzlocal
	$(PY3_VENV)/bin/python3 -munittest discover -s $(UNIT_DIR) $(TESTOPTS)
	rm -rf $(PY3_VENV)

.PHONY: upload
upload: test-unit test-integration
	python3 setup.py sdist --dist-dir $(TMP) upload

$(INTEGRATION_DIR)/utt-$(VERSION).tar.gz: sdist
	cp $(TMP)/utt-$(VERSION).tar.gz $@
