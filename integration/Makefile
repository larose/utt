UTT_DATA_FILENAME = /.local/share/utt/utt.log
UTT = /usr/local/bin/utt

all: add hello smoke-test report-1 report-uppercase

$(UTT):
	python setup.py install build --build-base /tmp/build install

add: $(UTT)
	@echo
	@echo ">> ADD"

	rm -f $(UTT_DATA_FILENAME)
	utt --now "2014-01-01 8:00" add "  spaces  "
	utt --now "2014-01-01 9:00" add "utt: programming"

	bash -c 'diff $(UTT_DATA_FILENAME) data/add/utt.log'

	@echo "<< ADD"

bash:
	bash -i

hello: $(UTT)
	@echo
	@echo ">> HELLO"

	rm -f $(UTT_DATA_FILENAME)
	utt --now "2014-01-01 8:00" hello
	utt --now "2014-01-01 9:00" hello

	bash -c 'diff $(UTT_DATA_FILENAME) data/hello/utt.log'

	@echo "<< HELLO"

smoke-test: $(UTT)
	@echo
	@echo ">> SMOKE TEST"

	PYTHONIOENCODING=utf_8 utt stretch
	EDITOR=true utt edit

	@echo "<< SMOKE TEST"

report-1: $(UTT)
	@echo
	@echo ">> REPORT-1"

	cp data/utt-1.log $(UTT_DATA_FILENAME)
	bash -c 'diff <(utt --now "2014-3-19 18:30" report 2014-3-19) data/utt-1.stdout'

	@echo "<< REPORT-1"

report-uppercase: $(UTT)
	@echo
	@echo ">> REPORT-UPPERCASE"

	cp data/utt-upper-case.log $(UTT_DATA_FILENAME)
	bash -c 'diff <(utt --now "2014-3-14 12:00" report 2014-3-14 --no-current-activity) data/utt-upper-case.stdout'

	@echo "<< REPORT-UPPERCASE"

.PHONY: all add bash hello smoke-test report-1 report-uppercase
