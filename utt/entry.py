class Entry:
    def __init__(self, datetime, name, is_current_entry, comment=None):
        self.datetime = datetime
        self.name = name
        self.is_current_entry = is_current_entry
        self.comment = comment

    def __str__(self):
        str_components = [
            self.datetime.strftime("%Y-%m-%d %H:%M%z"), self.name
        ]

        if self.comment:
            str_components.append("".join([" # ", self.comment]))

        return " ".join(str_components)
