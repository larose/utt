import datetime

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# PUBLIC
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def parse_datetime(datetimestring):
    return datetime.datetime.strptime(datetimestring, "%Y-%m-%d %H:%M")
