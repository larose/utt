Ultimate Time Tracker
======================

Ultimate Time Tracker (utt) is a simple command-line time tracking
application written in Python.

- [Quick Start](#quick-start)
- [Commands](#commands)
    - [`hello`](#hello)
    - [`add`](#add)
        - [Activity Type](#activity-type)
    - [`edit`](#edit)
    - [`report`](#report)
        - [Sections](#sections)
        - [Report Date](#report-date)
        - [Current Activity](#current-activity)
        - [Weekly Working and Break Times](#weekly-working-and-break-times)
    - [`stretch`](#stretch)
- [Configuration](#configuration)
- [Bash Completion](#bash-completion)
- [Development](#development)
    - [Dependencies](#dependencies)
    - [Format code](#format-code)
    - [Lint](#lint)
    - [Executing `utt` from source](#executing-utt-from-source)
    - [Tests](#tests)
        - [Unit Tests](#unit-tests)
        - [Integration Tests](#integration-tests)
- [Contributors](#contributors)
- [License](#license)
- [Website](#website)


## Quick Start

Install `utt` from PyPI:

`$ pip install utt`

Note: `utt` is compatible with Python 2 and Python 3.


### hello

Say hello when you arrive in the morning:

`$ utt hello`


### add

Add a task when you have finished working on it:

`$ utt add "programming"`


### report

Show report:

```
$ utt report

------------------------ Monday, Jul 08, 2013 (week 28) ------------------------

Working Time: 0h07
Break   Time: 0h00

----------------------------------- Projects -----------------------------------

(0h07) : programming

---------------------------------- Activities ----------------------------------

(0h07) : programming


----------------------------------- Details ------------------------------------

(0h07) 08:27-08:34 programming
```


### edit

Edit your timesheet:

`$ utt edit`


## Commands

### `hello`

`$ utt hello` should be the first command you execute when you start
your day. It tells `utt` that you are now tracking your time.

Example:

```
$ utt hello
```

### `add`

When you have completed a task, add it to `utt` with the `add`
command.

Example:

`$ utt add programming`

You add a task when you have completed it, not when you start doing
it.

#### Activity Type

There are three types of activities: working, break and
ignored. Working activities contribute to the working time, break
activities to the break time and ignored activities to neither. This
feature is very useful when viewing your timesheet with the `report`
command as it enables `utt` to group your activities by type.

The activity type is defined by its name. If it ends with `**` it's a
break activity. If it ends with `***` it's an ignored
activity. Otherwise, it's a working activity.

Examples:


- Working activity

```
$ utt add "task #4"
```

- Break activity

```
$ utt add "lunch **"
```

- Ignored activity

```
$ utt add "commuting ***"
```


### `edit`

`edit` opens your timesheet in a text editor so you can edit it.

Example:

```
$ utt edit
```

`utt` opens the text editor defined by the environment variable
`$VISUAL` and, if not set, by the environment variable `$EDITOR`. If
neither is set, `utt` opens `vi`.


### `report`

`$ utt report` shows your timesheet.

Examples:

- Timesheet for today: `$ utt report`

- Timesheet for a specific date: `$ utt report 2018-03-25`

- Timesheet for a period: `$ utt report --from 2018-10-22 --to 2018-10-26`



#### Sections

There are four sections in a report. As we will see, each one is a
aggregated view of the previous one.

1. Summary: shows the report date and the total working and break
time.

2. Projects: groups activities by project. This is useful to track the
total time by projects. We will see how to specify the project for an
activity.

3. Activities: groups activities by name. This is useful to track the
total time worked on a task when you have worked on it multiple times.

4. Details: timeline of your activities.


Let's look at an example. Let's say you entered those activities
throughout the day:

```
$ utt hello
$ utt add "project-1: task-3"
$ utt add "project-2: task-2"
$ utt add "project-1: task-1"
$ utt add "lunch **"
$ utt add "project-2: task-2"
$ utt add "project-1: task-2"
```

And then you view your timesheet:

```
$ utt report

----------------------- Saturday, Nov 03, 2018 (week 44) -----------------------

Working Time: 7h00 [7h00]
Break   Time: 1h00 [1h00]

----------------------------------- Projects -----------------------------------

(5h00) project-1: task-1, task-2, task-3
(2h00) project-2: task-2

---------------------------------- Activities ----------------------------------

(2h15) project-1: task-1
(2h15) project-1: task-2
(0h30) project-1: task-3
(2h00) project-2: task-2

(1h00) : lunch **

----------------------------------- Details ------------------------------------

(0h30) 09:00-09:30 project-1: task-3
(0h15) 09:30-09:45 project-2: task-2
(2h15) 09:45-12:00 project-1: task-1
(1h00) 12:00-13:00 lunch **
(1h45) 13:00-14:45 project-2: task-2
(2h15) 14:45-17:00 project-1: task-2
```

The first section, the summary section, shows that you worked 7h and
had a 1-hour break.

Then, the projects section shows that you worked 5h on project 1 and
2h on project 2. You can specify the project of an activity by
prefixing it with a non-whitespace string followed by a colon (e.g
`project-1:`, `project2:`).

The next section, the activities section, shows how long you worked on
each activity. For instance, even though you worked twice on
`project-2: task-2` (0h15 + 1h45), it is shown once in that section.

Finally, the details section shows a timeline of all your activity.


#### Report Date

You can choose the report date by passing a date to the `report`
command. The date must be either an absolute date formatted as
"%Y-%m-%d" or a day of the week.

Examples:

Absolute date:

```
$ utt report 2013-07-01
```

Day of the week:

```
$ utt report monday
```

If today is Wednesday, Feb 18, the report date is Monday, Feb 16.

You can also specify a date range. All the activities will be aggregated for
the given time period.

To report activities from 2013-07-01 00:00:00 to 2013-12-31 23:59:59 :
```
$ utt report --from 2013-07-01 --to 2013-12-31
```

To report activities since Monday:
```
$ utt report --from monday
```


#### Current Activity

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


#### Weekly Working and Break Times

The time reported in the square brackets is the total time for the
week.

```
$ utt report

----------------------- Tuesday, Mar 25, 2014 (week 13) ------------------------

Working Time: 1h00 [8h00]
Break   Time: 0h00 [0h30]

...
```


### `stretch`

Stretch the latest task to the current time:

Example:

```
$ utt stretch
stretched 2013-07-08 08:34 programming
        → 2013-07-08 09:00 programming
```

## Configuration

### Timezone

Warning: timezone is an experimental feature.

To enable timezone support, get the config filename:

```
$ utt config --filename
`/home/<user>/.config/utt/utt.cfg`
```

Then, open it with a text editor and change it so it looks like this:

```
[timezone]
enabled = true
```

## Bash Completion

`utt` uses [argcomplete](https://github.com/kislyuk/argcomplete) to
provide bash completion.

First, make sure
[`bash-completion`](https://github.com/scop/bash-completion) is
installed:

- Fedora: `$ sudo dnf install bash-completion`
- Ubuntu: `$ sudo apt-get install bash-completion`


Then execute:

```
$ register-python-argcomplete utt >> ~/.bashrc
```

Finally, start a new shell.

## Development

### Dependencies

- Python 3
- [Make](https://www.gnu.org/software/make/)
- [Pipenv](https://pipenv.readthedocs.io/en/latest/)
- [Docker](https://www.docker.com/)

### Format code

To format code:

`$ make format`


### Lint

To lint code:

`$ make lint`

### Executing `utt` from source

To run `utt` from local source:

`$ pipenv run ./run`

### Tests

To execute unit and integration tests:

`$ make test`

#### Unit Tests

`$ make test-unit`

#### Integration Tests

To run integration tests for Python 2 and Python 3:

`$ make test-integration`

This will create two Docker containers, one for each version of
Python, and run all the tests in `test/integration/Makefile`.

To run integration tests for Python 2 only:

`$ make test-integration-py2`

To run integration tests for Python 3 only:

`$ make test-integration-py3`

To run a specific test:

`$ make test-integration INTEGRATION_CMD=hello`


## Contributors

- Mathieu Larose <<mathieu@mathieularose.com>>
- David Munger <<mungerd@gmail.com>>
- Paul Ivanov <<pi@berkeley.edu>>
- Jason Stewart <<support@eggplantsd.com>>
- Kit Choi <<kit@kychoi.org>>
- Henrik Holm <<ukrutt@gmail.com>>
- Stephan Gross <<stephangross6@gmail.com>>


## License

utt is released under the GPLv3. See the LICENSE file for details.


## Website

http://github.com/larose/utt
