class Entry:
    def __init__(self, datetime, name, is_current_entry):
        self.datetime = datetime
        self.name = name
        self.is_current_entry = is_current_entry

    def __str__(self):
        return " ".join(
            [self.datetime.strftime("%Y-%m-%d %H:%M%z"), self.name])
