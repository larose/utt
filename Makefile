TMPDIR = tmp
CONTAINER_DATA_FILENAME = $(TMPDIR)/integration/py$*/utt
CONTAINER_NAME = utt-integration-py$*
FILES := bin CHANGES LICENSE MANIFEST.in README.md setup.py integration/Makefile integration/data

all:

integration: integration-py2 integration-py3

integration-py%: integration-container-py%
	docker run --rm -ti -e PYTHON_VERSION=$* $(CONTAINER_NAME)

integration-clean:
	rm -rf $(TMPDIR)/integration

integration-data-py%:
	mkdir -p $(CONTAINER_DATA_FILENAME)
	rsync -rtm --delete $(FILES) $(CONTAINER_DATA_FILENAME)
	rsync -rtm --delete --include "*.py" --exclude "*.*" utt $(CONTAINER_DATA_FILENAME)

integration-container-py%: integration-data-py% $(TMPDIR)/integration/py%/Dockerfile
	docker build -t $(CONTAINER_NAME) $(TMPDIR)/integration/py$*

unit:
	python3 -munittest $(TESTOPTS)

$(TMPDIR)/integration/py%/Dockerfile: integration/Dockerfile.template
	sed -e "s/{{PYTHON_VERSION}}/$*/" $< > $@


.PHONY: all integration integration-clean unit
