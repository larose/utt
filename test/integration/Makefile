UTT_DATA_FILENAME = $(HOME)/.local/share/utt/utt.log
UTT = /usr/local/bin/utt

.PHONY: all
all: add edit hello stretch report-1 report-dayname report-uppercase report-range version

$(UTT):
	$(PIP) install utt-*.tar.gz

.PHONY: add
add: $(UTT)
	@echo
	@echo ">> ADD"

	rm -f $(UTT_DATA_FILENAME)
	utt --now "2014-01-01 8:00" add "  spaces  "
	utt --now "2014-01-01 9:00" add "utt: programming"
	utt --now "2014-01-02 8:00" add "utt: programming"
	utt --now "2014-01-02 9:00" add "utt: programming"

	bash -c 'diff $(UTT_DATA_FILENAME) data/add/utt.log'

	@echo "<< ADD"

.PHONY: edit
edit: $(UTT)
	@echo
	@echo ">> EDIT"

	mkdir -p `dirname $(UTT_DATA_FILENAME)`
	cp data/hello/utt.log  $(UTT_DATA_FILENAME)
	bash -c 'diff <(EDITOR=cat utt edit) data/hello/utt.log'

	@echo "<< EDIT"

.PHONY: hello
hello: $(UTT)
	@echo
	@echo ">> HELLO"

	rm -f $(UTT_DATA_FILENAME)
	utt --now "2014-01-01 8:00" hello
	utt --now "2014-01-01 9:00" hello
	utt --now "2014-01-02 8:00" hello
	utt --now "2014-01-02 9:00" hello

	bash -c 'diff $(UTT_DATA_FILENAME) data/hello/utt.log'

	@echo "<< HELLO"

.PHONY: stretch
stretch: $(UTT)
	@echo
	@echo ">> STRETCH"

	mkdir -p `dirname $(UTT_DATA_FILENAME)`
	cp data/stretch/before.log $(UTT_DATA_FILENAME)
	bash -c 'diff <(PYTHONIOENCODING=utf_8 utt --now "2014-01-01 10:00" stretch) data/stretch/stdout'
	bash -c 'diff $(UTT_DATA_FILENAME) data/stretch/after.log'

	@echo "<< STRETCH"

.PHONY: report-1
report-1: $(UTT)
	@echo
	@echo ">> REPORT-1"

	cp data/utt-1.log $(UTT_DATA_FILENAME)
	bash -c 'diff <(utt --now "2014-3-19 18:30" report 2014-3-19) data/utt-1.stdout'

	@echo "<< REPORT-1"

.PHONY: report-dayname
report-dayname: $(UTT)
	@echo
	@echo ">> REPORT-DAYNAME"

	utt --now "2015-2-16 12:00" report thursday | grep ^- | head -n 1 | diff data/report/dayname -

	@echo "<< REPORT-DAYNAME"

.PHONY: report-uppercase
report-uppercase: $(UTT)
	@echo
	@echo ">> REPORT-UPPERCASE"

	cp data/utt-upper-case.log $(UTT_DATA_FILENAME)
	bash -c 'diff <(utt --now "2014-3-14 12:00" report 2014-3-14 --no-current-activity) data/utt-upper-case.stdout'

	@echo "<< REPORT-UPPERCASE"

report-range: $(UTT)
	@echo
	@echo ">> REPORT-RANGE"

	cp data/utt-1.log $(UTT_DATA_FILENAME)
	bash -c 'diff <(utt --now "2014-3-14 12:00" report --from 2014-3-14 --to 2014-03-19 --no-current-activity) data/utt-range.stdout'

	@echo "<< REPORT-UPPERCASE"

.PHONY: version
version: $(UTT)
	@echo
	@echo ">> VERSION"

	utt --version

	@echo "<< VERSION"


.PHONY: shell
shell:
	bash
