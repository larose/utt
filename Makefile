CONTAINER_DATA_FILENAME = integration/py$*/utt
CONTAINER_NAME = utt-integration-py$*
FILES := bin CHANGES LICENSE MANIFEST.in README.md setup.py integration/Makefile integration/data

all:

integration: integration-py2 integration-py3

integration-py%: integration-container-py%
	docker run --rm -ti -e PYTHON=python$* $(CONTAINER_NAME)

integration-clean:
	rm -rf integration/*/utt

integration-data-py%: integration/py%/utt
	rsync -rtm --delete $(FILES) $(CONTAINER_DATA_FILENAME)
	rsync -rtm --delete --include "*.py" --exclude "*.*" utt $(CONTAINER_DATA_FILENAME)

integration-container-py%: integration-data-py%
	docker build -t $(CONTAINER_NAME) integration/py$*

integration/%/utt:
	mkdir -p $@

unit:
	python3 -munittest $(TESTOPTS)


.PHONY: all integration integration-clean unit

.PRECIOUS: integration/py2/utt integration/py2/utt/setup.py integration/py2/utt/MANIFEST.in integration/py2/utt/CHANGES integration/py2/utt/LICENSE integration/py2/utt/Makefile integration/py2/utt/README.md integration/py2/utt/data integration/py3/utt integration/py3/utt/setup.py integration/py3/utt/MANIFEST.in integration/py3/utt/CHANGES integration/py3/utt/LICENSE integration/py3/utt/Makefile integration/py3/utt/README.md integration/py3/utt/data
