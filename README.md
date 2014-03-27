Ultimate Time Tracker
======================

Ultimate Time Tracker (utt) is a minimalist command-line time tracking
application written in Python. It is intended for people who need to
report their time on another system and want a preliminary time sheet.


## Usage

There are four commands in utt: `hello`, `add`, `report` and `edit`.

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

Edit your time sheet with your favorite text editor:


`$ utt edit`

### Activity

An activity name does more than just identifying it. It's used to
determine its type and to group them.

There are three activity types: working, break, ignored.

#### Working

This is the default activity. It contributes to the working time.

```
$ utt add "task #4"
```

#### Break

Activity whose name ends with `**`. It contributes to the break time.

Example:

```
$ utt add "lunch **"
```

#### Ignored

Activity whose name ends with `***`. Only shown in the "Detail
section".

Example:

```
$ utt add "ignored activity ***"
```


### Report

#### Grouping by project

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

If multiple activities have the same name, they are merged as one
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

#### Selecting the date of the report

The `report` command let you choose the date of the report. If
omitted, it's the current date.

Example:

```
$ utt report 2013-07-01
```

#### Current activity

A `-- Current Activity --` is inserted if the date of the report is
today.

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

#### Weekly working and break times

The time reported in the square brackets is the total time for the
week.

```
$ utt report

----------------------- Tuesday, Mar 25, 2014 (week 13) ------------------------

Working Time: 1h00 [8h00]
Break   Time: 0h00 [0h30]

...
```

## Installation

### `pip`

`$ pip install utt`

utt is only compatible with Python 3. Make sure you are using `pip`
with Python 3.

### `setup.py`

`python3 setup.py install`


## Requirements

Python 3


## Author

Mathieu Larose <<mathieu@mathieularose.com>>


## License

utt is released under the GPLv3. See the LICENSE file for details.


## Website

http://github.com/larose/utt
