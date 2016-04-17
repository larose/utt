INTEGRATION_DIR = test/integration
UNIT_DIR = test/unit
TMP = tmp
CONTAINER_NAME = utt-integration-py$*
VERSION := $(shell python3 setup.py --version)

.PHONY: all
all:

.PHONY: clean
clean:
	rm -rf $(TMP)
	rm -f $(INTEGRATION_DIR)/utt-*.tar.gz

.PHONY: integration
integration: integration-py2 integration-py3

.PHONY: integration-py%
integration-py%: integration-container-py%
	docker run --rm -ti -v "$(CURDIR)/$(INTEGRATION_DIR):/utt:ro" $(CONTAINER_NAME) $(INTEGRATION_CMD)

.PHONY: integration-container-py%
integration-container-py%: $(INTEGRATION_DIR)/utt-$(VERSION).tar.gz
	docker build -t $(CONTAINER_NAME) -f $(INTEGRATION_DIR)/Dockerfile.py$* $(INTEGRATION_DIR)

.PHONY: sdist
sdist:
	mkdir -p $(TMP)
	python3 setup.py sdist --dist-dir $(TMP) --manifest $(TMP)/MANIFEST

.PHONY: test
test: integration unit

.PHONY: unit
unit:
	python3 -munittest discover -s $(UNIT_DIR) $(TESTOPTS)

.PHONY: upload
upload: unit integration
	python3 setup.py sdist --dist-dir $(TMP) --manifest $(TMP)/MANIFEST upload

$(INTEGRATION_DIR)/utt-$(VERSION).tar.gz: sdist
	cp $(TMP)/utt-$(VERSION).tar.gz $@
