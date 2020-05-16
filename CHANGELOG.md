## 1.24 (2020-05-16)

  * Migrate from Pipenv to Poetry
  * Migrate from CircleCI to GitHub Actions

## 1.23 (2020-05-09)

  * utt report --week now works on Python 3.7

## 1.22 (2020-04-05)

  * Warn if Python version is unsupported.
  * [Security] Bump bleach from 3.1.2 to 3.1.4.

## 1.21 (2020-03-29)

  * Plugins can now register components

## 1.19 (2020-03-14)

  * Prevent EINVAL when reading empty log file

## 1.18 (2020-01-01)

  * Add plugin support

## 1.17 (2019-12-27)

  * Drop Python 2 support

## 1.16 (2019-12-24)

  * Add ability to comment/annotate an entry

## 1.15 (2019-12-14)

  * Add month and week switch to filter by month and week
  * Add csv switch to output in csv

## 1.14 (2019-12-07)

  * Add `--details` flag to show details even on multi-day reports

## 1.13 (2019-11-27)

  * Add switches to report for specific project, and also hours worked
    per day

## 1.12 (2018-11-11)

  * Format duration > 24h as hours instead of days

## 1.11 (2018-11-11)

  * Fix current activity start time when previous entry is "hello"

## 1.10 (2018-11-10)

  * utt now works on Windows

## 1.9 (2018-11-04)

  * Add timezone support (experimental)
  * Range report accepts day of week

## 1.8 (2018-08-31)

  * Add range report
  * Add overnight activity support

## 1.7 (2017-05-21)

  * Add bash completion

## 1.6 (2016-04-17)

  * Strech appends an entry instead of modifying the latest entry
    in-place

## 1.5 (2016-04-10)

  * Insert a blank line between days in log file
  * Add argument --version

## 1.4 (2015-02-15)

  * Report accepts days of the week
  * Align project name to the left

## 1.3 (2014-09-30)

  * Add Python 2 compatibility
  * Add argument --now

## 1.2 (2014-09-08)

  * Add stretch command
  * Name and project are case insensitive

## 1.1 (2014-03-27)

  * Add weekly working and break times

## 1.0 (2013-07-21)

  * Original implementation
