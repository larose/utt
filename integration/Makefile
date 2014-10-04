UTT_DATA_FILENAME = /.local/share/utt/utt.log
UTT = /usr/local/bin/utt

all: smoke-test report-1 report-uppercase

$(UTT):
	python setup.py install build --build-base /tmp/build install

bash:
	bash -i

smoke-test: $(UTT)
	@echo
	@echo ">> SMOKE TEST"

	utt hello
	utt add foo
	PYTHONIOENCODING=utf_8 utt stretch
	EDITOR=true utt edit
	utt report

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

.PHONY: all bash smoke-test report-1 report-uppercase
