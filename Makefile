TMP = tmp
TEST_TMP = $(TMP)/integration
CONTAINER_DATA_FILENAME = $(TEST_TMP)/py$*/utt
CONTAINER_NAME = utt-integration-py$*
FILES := bin CHANGES LICENSE MANIFEST.in README.md setup.py integration/Makefile integration/data

all:

integration: integration-py2 integration-py3

integration-py%: integration-container-py%
	docker run --rm -ti -e PYTHON_VERSION=$* $(CONTAINER_NAME) $(INTEGRATION_CMD)

integration-clean:
	rm -rf $(TEST_TMP)

integration-data-py%:
	mkdir -p $(CONTAINER_DATA_FILENAME)
	rsync -rtm --delete $(FILES) $(CONTAINER_DATA_FILENAME)
	rsync -rtm --delete --include "*.py" --exclude "*.*" utt $(CONTAINER_DATA_FILENAME)

integration-container-py%: integration-data-py% $(TEST_TMP)/py%/Dockerfile
	docker build -t $(CONTAINER_NAME) $(TEST_TMP)/py$*

unit:
	python3 -munittest $(TESTOPTS)

$(TEST_TMP)/py%/Dockerfile: integration/Dockerfile.template
	sed -e "s/{{PYTHON_VERSION}}/$*/" $< > $@


.PHONY: all integration integration-clean unit
