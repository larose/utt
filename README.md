Ultimate Time Tracker
======================

Ultimate Time Tracker (utt) is a simple command-line time tracking
application written in Python.

## Contents

- [Quick start](#quick-start)
    - [hello](#hello)
    - [add](#add)
    - [report](#report)
    - [edit](#edit)
    - [stretch](#stretch)
- [Usage](#usage)
    - [Activity](#activity)
    - [Report](#report)
- [Bash completion](#bash-completion)
- [Development](#development)
- [Contributors](#contributors)
- [License](#license)
- [Website](#website)


## Quick start

Install `utt` from PyPI:

`$ pip install utt`

Note: utt is compatible with both Python 2 and Python 3.


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

Edit your time sheet with your favorite text editor (according to the
`EDITOR` environment variable):

`$ utt edit`


### stretch

Stretch the latest task to the current time:

```
$ utt stretch
stretched 2013-07-08 08:34 programming
        → 2013-07-08 09:00 programming
```


## Usage

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


#### Choosing the report date

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
the given time period. The date must be an absolute date formatted as
"%Y-%m-%d".

To report activities from 2013-07-01 00:00:00 to 2013-12-31 23:59:59 :
```
$ utt report --from 2013-07-01 --to 2013-12-31
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

## Bash completion

`utt` uses [argcomplete](https://github.com/kislyuk/argcomplete) to
provide bash completion.

First, make sure
[`bash-completion`](https://github.com/scop/bash-completion) is
installed:

- Fedora: `$ sudo dnf install bash-completion`
- Ubuntu: `$ sudo apt-get install bash-completion`


Then execute:

```
$ sudo activate-global-python-argcomplete
```

Finally, start a new shell or execute `source /etc/profile`.

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

#### Integration tests

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


## License

utt is released under the GPLv3. See the LICENSE file for details.


## Website

http://github.com/larose/utt
