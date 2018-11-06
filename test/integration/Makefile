UTT_DATA_FILENAME = $(HOME)/.local/share/utt/utt.log
UTT = /usr/local/bin/utt

.PHONY: all
all: add \
  completion \
  edit \
  hello \
  stretch \
  report-1 \
  report-dayname \
  report-no-current-activity \
  report-uppercase \
  report-range report-overnight \
  report-overnight-range \
  report-change-timezone \
  report-timezone-daylight-change \
  version

$(UTT):
	$(PIP) install utt-*.whl

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

.PHONY: completion
completion: $(UTT)
	# @echo
	# @echo ">> COMPLETION"

	# head -c 1024 `which utt` | grep "PYTHON_ARGCOMPLETE_OK"
	# activate-global-python-argcomplete
	# bash --login -i -c 'diff <(COMP_LINE="utt" COMP_POINT=4 _python_argcomplete_global utt && echo $${COMPREPLY[@]}) <(echo -h --help --data --now --timezone --version add config edit hello report stretch)'

	# @echo "<< COMPLETION"


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

.PHONY: report-no-current-activity
report-no-current-activity:
	@echo
	@echo ">> REPORT-NO-CURRENT-ACTIVITY"

	mkdir -p `dirname $(UTT_DATA_FILENAME)`
	cp data/utt-no-current-activity.log $(UTT_DATA_FILENAME)
	bash -c 'diff <(utt --now "2018-08-21 20:00" report 2018-08-20) data/utt-no-current-activity.stdout'

	@echo "<< REPORT-NO-CURRENT-ACTIVITY"

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
	bash -c 'diff <(utt --now "2014-3-19 18:30" report --from 2014-3-15 --to 2014-03-19 --no-current-activity) data/utt-range.stdout'

	@echo "<< REPORT-UPPERCASE"

report-overnight: $(UTT)
	@echo
	@echo ">> REPORT-OVERNIGHT"

	cp data/utt-overnight.log $(UTT_DATA_FILENAME)
	bash -c 'diff <(utt --now "2014-3-19 18:30" report "2014-03-14") data/utt-overnight.stdout'

	@echo "<< REPORT-OVERNIGHT"


report-overnight-range: $(UTT)
	@echo
	@echo ">> REPORT-OVERNIGHT-RANGE"

	cp data/utt-overnight.log $(UTT_DATA_FILENAME)
	bash -c 'diff <(utt --now "2014-3-19 18:30" report --from "2014-03-14" --to "2014-03-18") data/utt-overnight-range.stdout'

	@echo "<< REPORT-OVERNIGHT-RANGE"

report-change-timezone: $(UTT)
	@echo
	@echo ">> REPORT-CHANGE-TIMEZONE"

	cp data/utt-change-timezone.log $(UTT_DATA_FILENAME)
	bash -c 'diff <(utt --now "2018-08-10 18:00" report "2018-08-08") data/utt-change-timezone.stdout'

	@echo "<< REPORT-CHANGE-TIMEZONE"


.PHONY: report-timezone-daylight-change
report-timezone-daylight-change: $(UTT)
	@echo
	@echo ">> REPORT-TIMEZONE-DAYLIGHT-CHANGE"

	mkdir -p `dirname $(UTT_DATA_FILENAME)`
	rm -f $(UTT_DATA_FILENAME)
	echo "2018-10-28 08:00+0800 hello" >> $(UTT_DATA_FILENAME)
	echo "2018-10-28 12:00+0800 travel" >> $(UTT_DATA_FILENAME)

	utt --now "2018-10-28 18:30" --timezone "Europe/London" report --no-current-activity

	bash -c 'diff <(utt --now "2018-10-28 18:30" --timezone "Europe/London" report --no-current-activity) data/utt-report-timezone-daylight-change.stdout'

	@echo "<< REPORT-TIMEZONE-DAYLIGHT-CHANGE"


.PHONY: version
version: $(UTT)
	@echo
	@echo ">> VERSION"

	utt --version

	@echo "<< VERSION"


.PHONY: shell
shell:
	bash
