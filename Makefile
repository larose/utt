all:

test:
	python3 -munittest $(TESTOPTS)

.PHONY: all test
