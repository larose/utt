INTEGRATION_DIR = test/integration
UNIT_DIR = test/unit
TMP = tmp
TEST_TMP = $(TMP)/integration
CONTAINER_DATA_DIR = $(TEST_TMP)/py$*
CONTAINER_NAME = utt-integration-py$*
TEST_FILES := $(INTEGRATION_DIR)/Makefile $(INTEGRATION_DIR)/data
VERSION := $(shell cat VERSION)

all:

clean:
	rm -rf $(TMP)

integration: integration-py2 integration-py3

integration-py%: integration-container-py%
	docker run --rm -ti -v "$(CURDIR)/$(CONTAINER_DATA_DIR)/tarball:/utt/tarball:ro" $(CONTAINER_NAME) $(INTEGRATION_CMD)

integration-data-py%: $(TEST_TMP)/py%/tarball/utt-$(VERSION).tar.gz
	mkdir -p $(CONTAINER_DATA_DIR)
	rsync -rtm --delete $(TEST_FILES) $(CONTAINER_DATA_DIR)

integration-container-py%: integration-data-py% $(TEST_TMP)/py%/Dockerfile
	docker build -t $(CONTAINER_NAME) $(TEST_TMP)/py$*

sdist:
	mkdir -p $(TMP)
	python3 setup.py sdist --dist-dir $(TMP) --manifest $(TMP)/MANIFEST

unit:
	python3 -munittest discover -s $(UNIT_DIR) $(TESTOPTS)

$(TEST_TMP)/py%/Dockerfile: $(INTEGRATION_DIR)/Dockerfile.py%
	mkdir -p $(CONTAINER_DATA_DIR)
	cp $< $@

$(TEST_TMP)/py%/tarball/utt-$(VERSION).tar.gz: sdist
	mkdir -p $(CONTAINER_DATA_DIR)/tarball
	cp $(TMP)/utt-$(VERSION).tar.gz $@

.PHONY: all clean integration dist unit
