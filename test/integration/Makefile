UTT_DATA_FILENAME = $(HOME)/.local/share/utt/utt.log
UTT = /usr/local/bin/utt

.PHONY: all
all: add \
  completion \
  edit \
  example-plugin \
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
  report-hello-only-today \
  report-project \
  report-per-day \
  report-project-per-day \
  report-project-per-day-csv \
  report-project-per-day-csv-2 \
  report-per-day-csv \
  report-month \
  report-details \
  report-comments \
  report-week-current \
  version

$(UTT):
	pip install utt-*.whl

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
	@echo
	@echo ">> COMPLETION"

	register-python-argcomplete utt >> ~/.bashrc
	bash -i -c 'diff <(COMP_LINE="utt" COMP_POINT=4 _python_argcomplete utt && echo $${COMPREPLY[@]} | tr " " "\n" | sort) <(echo -h --help --data --now --timezone --version add config edit hello report stretch | tr " " "\n" | sort)'

	@echo "<< COMPLETION"


.PHONY: edit
edit: $(UTT)
	@echo
	@echo ">> EDIT"

	mkdir -p `dirname $(UTT_DATA_FILENAME)`
	cp data/hello/utt.log  $(UTT_DATA_FILENAME)
	bash -c 'diff <(EDITOR=cat utt edit) data/hello/utt.log'

	@echo "<< EDIT"

.PHONY: empty-file
empty-file: $(UTT)
	@echo
	@echo ">> EMPTY FILE"

	mkdir -p `dirname $(UTT_DATA_FILENAME)`
	echo -n "" > $(UTT_DATA_FILENAME)
	utt hello

	@echo "<< EMPTY FILE"

.PHONY: example-plugin
example-plugin: $(UTT)
	@echo
	@echo ">> EXAMPLE PLUGIN"

	cd utt_example_plugin && python3 setup.py install --record utt_example_files
	bash -c 'diff <(utt --now "2020-01-03 9:00" foo) <(echo Now: 2020-01-03 09:00:00+00:00)'
	rm -f $(UTT_DATA_FILENAME)
	utt --now "2020-01-03 9:00" hello
	utt --now "2020-01-03 10:00" add work
	bash -c 'diff <(utt --now "2020-01-03 10:30" report) data/utt-example-plugin-report.stdout'
	cd utt_example_plugin && cat utt_example_files | xargs rm -rf

	@echo "<< EXAMPLE PLUGIN"

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

	mkdir -p `dirname $(UTT_DATA_FILENAME)`
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
report-no-current-activity: $(UTT)
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

	mkdir -p `dirname $(UTT_DATA_FILENAME)`
	cp data/utt-upper-case.log $(UTT_DATA_FILENAME)
	bash -c 'diff <(utt --now "2014-3-14 12:00" report 2014-3-14 --no-current-activity) data/utt-upper-case.stdout'

	@echo "<< REPORT-UPPERCASE"

report-range: $(UTT)
	@echo
	@echo ">> REPORT-RANGE"

	mkdir -p `dirname $(UTT_DATA_FILENAME)`
	cp data/utt-1.log $(UTT_DATA_FILENAME)
	bash -c 'diff <(utt --now "2014-3-19 18:30" report --from 2014-3-15 --to 2014-03-19 --no-current-activity) data/utt-range.stdout'

	@echo "<< REPORT-UPPERCASE"

report-overnight: $(UTT)
	@echo
	@echo ">> REPORT-OVERNIGHT"

	mkdir -p `dirname $(UTT_DATA_FILENAME)`
	cp data/utt-overnight.log $(UTT_DATA_FILENAME)
	bash -c 'diff <(utt --now "2014-3-19 18:30" report "2014-03-14") data/utt-overnight.stdout'

	@echo "<< REPORT-OVERNIGHT"


report-overnight-range: $(UTT)
	@echo
	@echo ">> REPORT-OVERNIGHT-RANGE"

	mkdir -p `dirname $(UTT_DATA_FILENAME)`
	cp data/utt-overnight.log $(UTT_DATA_FILENAME)
	bash -c 'diff <(utt --now "2014-3-19 18:30" report --from "2014-03-14" --to "2014-03-18") data/utt-overnight-range.stdout'

	@echo "<< REPORT-OVERNIGHT-RANGE"

report-change-timezone: $(UTT)
	@echo
	@echo ">> REPORT-CHANGE-TIMEZONE"

	mkdir -p `dirname $(UTT_DATA_FILENAME)`
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

	bash -c 'diff <(utt --now "2018-10-28 18:30" --timezone "Europe/London" report --no-current-activity) data/utt-report-timezone-daylight-change.stdout'

	@echo "<< REPORT-TIMEZONE-DAYLIGHT-CHANGE"

report-hello-only-today: $(UTT)
	@echo
	@echo ">> REPORT-HELLO-ONLY-TODAY"

	mkdir -p `dirname $(UTT_DATA_FILENAME)`
	cp data/utt-no-current-activity.log $(UTT_DATA_FILENAME)
	bash -c 'diff <(utt --now "2018-08-20 20:00" report 2018-08-20) data/utt-hello-only-today.stdout'

	@echo "<< REPORT-HELLO-ONLY-TODAY"

.PHONY: version
version: $(UTT)
	@echo
	@echo ">> VERSION"

	utt --version

	@echo "<< VERSION"


.PHONY: report-project
report-project: $(UTT)
	@echo
	@echo ">> REPORT-PROJECT"

	mkdir -p `dirname $(UTT_DATA_FILENAME)`
	cp data/utt-report-project.log $(UTT_DATA_FILENAME)
	bash -c 'diff -u <(utt --now "2018-08-20 20:00" report --project project_1) data/utt-report-project.stdout'

	@echo "<< REPORT-PROJECT"


.PHONY: report-per-day
report-per-day: $(UTT)
	# NOTE: this is not an intended use of the `--per-day` switch.
	#       It only really works well in conjunction with a
	#       `--project <proj_foo>` switch.  But it still works.
	@echo
	@echo ">> REPORT-PER-DAY"

	mkdir -p `dirname $(UTT_DATA_FILENAME)`
	cp data/utt-report-project.log $(UTT_DATA_FILENAME)
	bash -c 'diff -u <(utt --now "2018-08-21 20:00" report --from 2018-08-20 --to  2018-08-21 --per-day) data/utt-report-per-day.stdout'

	@echo "<< REPORT-PER-DAY"


.PHONY: report-project-per-day
report-project-per-day: $(UTT)
	@echo
	@echo ">> REPORT-PROJECT-PER-DAY"

	mkdir -p `dirname $(UTT_DATA_FILENAME)`
	cp data/utt-report-project.log $(UTT_DATA_FILENAME)
	bash -c 'diff -u <(utt --now "2018-08-21 20:00" report --from 2018-08-20 --to  2018-08-21 --project project_1 --per-day) data/utt-report-project-per-day.stdout'

	@echo "<< REPORT-PROJECT-PER-DAY"


.PHONY: report-project-per-day-csv
report-project-per-day-csv: $(UTT)
	@echo
	@echo ">> REPORT-PROJECT-PER-DAY-CSV"

	mkdir -p `dirname $(UTT_DATA_FILENAME)`
	cp data/utt-report-project.log $(UTT_DATA_FILENAME)
	bash -c 'diff -u --strip-trailing-cr <(utt --now "2018-08-21 20:00" report --from 2018-08-20 --to  2018-08-21 --project project_1 --csv-section per_day) data/utt-report-project-per-day-csv.csv'

	@echo "<< REPORT-PROJECT-PER-DAY-CSV"


# Like test above, but allow `--csv-section per-day` (not only `per_day`)
.PHONY: report-project-per-day-csv-2
report-project-per-day-csv-2: $(UTT)
	@echo
	@echo ">> REPORT-PROJECT-PER-DAY-CSV-2"

	mkdir -p `dirname $(UTT_DATA_FILENAME)`
	cp data/utt-report-project.log $(UTT_DATA_FILENAME)
	bash -c 'diff -u --strip-trailing-cr <(utt --now "2018-08-21 20:00" report --from 2018-08-20 --to  2018-08-21 --project project_1 --csv-section per-day) data/utt-report-project-per-day-csv.csv'

	@echo "<< REPORT-PROJECT-PER-DAY-CSV-2"


.PHONY: report-per-day-csv
report-per-day-csv: $(UTT)
	# NOTE: this is not an intended use of the `--csv-section` switch.
	#       It only really works well in conjunction with a
	#       `--project <proj_foo>` switch.  But it still works.
	@echo
	@echo ">> REPORT-PER-DAY-CSV"

	mkdir -p `dirname $(UTT_DATA_FILENAME)`
	cp data/utt-report-project.log $(UTT_DATA_FILENAME)
	bash -c 'diff -u --strip-trailing-cr <(utt --now "2018-08-21 20:00" report --from 2018-08-20 --to  2018-08-21 --csv-section per_day) data/utt-report-per-day-csv.csv'

	@echo "<< REPORT-PER-DAY-CSV"


.PHONY: report-month
report-month: $(UTT)
	@echo
	@echo ">> REPORT-MONTH"

	mkdir -p `dirname $(UTT_DATA_FILENAME)`
	cp data/utt-report-project.log $(UTT_DATA_FILENAME)
	bash -c 'diff -u <(utt --now "2018-09-21 20:00" report --month prev) data/utt-report-month.stdout'

	@echo "<< REPORT-MONTH"


.PHONY: report-details
report-details: $(UTT)
	@echo
	@echo ">> REPORT-DETAILS"

	mkdir -p `dirname $(UTT_DATA_FILENAME)`
	cp data/utt-report-project.log $(UTT_DATA_FILENAME)
	bash -c 'diff -u <(utt --now "2018-08-21 20:00" report --from 2018-08-20 --to 2018-08-21 --details) data/utt-report-details.stdout'

	@echo "<< REPORT-DETAILS"


.PHONY: report-comments
report-comments: $(UTT)
	@echo
	@echo ">> REPORT-COMMENTS"

	mkdir -p `dirname $(UTT_DATA_FILENAME)`
	cp data/utt-report-project.log $(UTT_DATA_FILENAME)
	bash -c 'diff -u <(utt --now "2018-08-21 20:00" report --from 2018-08-20 --to 2018-08-21 --details --comments) data/utt-report-comments.stdout'

	@echo "<< REPORT-COMMENTS"


.PHONY: report-week-current
report-week-current: $(UTT)
	@echo
	@echo ">> REPORT-WEEK-CURRENT"

	mkdir -p `dirname $(UTT_DATA_FILENAME)`
	cp data/utt-report-project.log $(UTT_DATA_FILENAME)
	bash -c 'diff -u <(utt --now "2018-08-21 20:00" report --week) data/utt-report-week-current.stdout'

	@echo "<< REPORT-WEEK-CURRENT"


.PHONY: shell
shell:
	bash
