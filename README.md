Ultimate Time Tracking
======================

Ultimate Time Tracking (utt) is a simple command-line time tracking
application. It's designed for users that need to report their time on
another system and want a preliminary timesheet.


## Usage

Say hello when you arrive in the morning:

`$ utt hello`

Add a task when you have finished working on it:

`$ utt add "configuring server"`

Show report:

```
$ utt report

------------------------ Monday, Jul 08, 2013 (week 28) ------------------------

Working Time: 0h07
Break   Time: 0h00

----------------------------------- Projects -----------------------------------

(0h07) : configuring server

---------------------------------- Activities ----------------------------------

(0h07) : configuring server


----------------------------------- Details ------------------------------------

(0h07) 08:27-08:34 configuring server
```

Edit your timesheet with your favorite text editor:


`$ utt edit`

These are the four commands available in utt.

### Report

The name of a activity is important. It's used to determine its type
(working, break, ignored) and to group them.

#### Type

There are three types:

* Working activity (default)
* Break activity (add `**` at the end of the name)
* Ignored activity (add `***` at the end of the name)

Ignored activities will only be shown in the "Details" section.

Example:

```
$ utt add "lunch **"
$ utt add "some task ***"
```

#### Grouping by projects

The "Projects" section of the report groups activities by projects. A
project can be associated to an activity by prefixing it with a
non-whitespace string followed by a colon.

Example:

```
$ utt add "#89"
$ utt add "project1: #43"
$ utt add "project1: #12"
$ utt add "project2: #63"
$ utt report
...

----------------------------------- Projects -----------------------------------

(0h30)         : #89
(0h45) project1: #12, #43
(1h00) project2: #63

---------------------------------- Activities ----------------------------------

(0h30)         : #89
(0h30) project1: #12
(0h15) project1: #43
(1h00) project2: #63

...
```

#### Grouping by name

If several activities have the same name, they will be merged as one
activity in the "Activities" section.

Example:

```
$ utt add "#83"
$ utt add "#26"
$ utt add "#83"

...

---------------------------------- Activities ----------------------------------

(1h00) : #26
(2h15) : #83


----------------------------------- Details ------------------------------------

(1h30) 08:30-10:00 #83
(1h00) 10:00-11:00 #26
(0h45) 11:00-11:45 #83
```

#### Changing the date of the report

The `report` command let you specify for which date you want the
report. If omitted, it's the current date.

Example:

```
$ utt report 2013-07-01
```

#### Current activity

By default, a `-- Current Activity--` is inserted if the date of the
report is today's date.

The first duration between the parentheses (1h00) represents the
working time without the current activity. The second duration between
the parentheses (0h22) represents the duration of the current
activity.

Example:

```
$ utt add "#12"
$ utt report

------------------------ Monday, Jul 08, 2013 (week 28) ------------------------

Working Time: 1h22 (1h00 + 0h22)
Break   Time: 0h00

----------------------------------- Projects -----------------------------------

(1h22) : #12, -- Current Activity --

---------------------------------- Activities ----------------------------------

(1h00) : #12
(0h22) : -- Current Activity --

...
```

You can change the current activity name with the `--current-activity`
argument.

Example:

```
$ utt report --current-activity "#76"

------------------------ Monday, Jul 08, 2013 (week 28) ------------------------

Working Time: 1h22 (1h00 + 0h22)
Break   Time: 0h00

----------------------------------- Projects -----------------------------------

(1h22) : #12, #76

---------------------------------- Activities ----------------------------------

(1h00) : #12
(0h22) : #76

...
```

Or, you can remove the current activity with the
`--no-current-activity` flag.

Example:

```
$ utt report --no-current-activity

------------------------ Monday, Jul 08, 2013 (week 28) ------------------------

Working Time: 1h00
Break   Time: 0h00

----------------------------------- Projects -----------------------------------

(1h00) : #12

---------------------------------- Activities ----------------------------------

(1h00) : #12
```

## Installation

`$ pip install utt`

utt is only compatible with Python 3. Make sure you are using `pip`
with Python 3.


## Requirements

Python 3


## Author

Mathieu Larose <mathieu@mathieularose.com>


## License

utt is released under the GPLv3. See the LICENSE file for details.


## Website

http://github.com/larose/utt
