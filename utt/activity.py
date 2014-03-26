from .name import Name


class Activity:
    class Type:
        WORK = 0
        BREAK = 1
        IGNORED = 2

    def __init__(self, previous_entry_time, entry):
        self.name = Name(entry.name)
        self.start = previous_entry_time
        self.end = entry.datetime
        self.duration = self.end - self.start
        self.type = Activity._type_from_name(entry.name)
        self.is_current_activity = entry.is_current_entry

    def __eq__(self, other):
        return self.name == other.name and \
            self.start == other.start and \
            self.end == other.end and \
            self.duration == other.duration and \
            self.type == other.type

    def __str__(self):
        return "Activity(" + ", ".join(map(str, [self.name,
                                                 self.start,
                                                 self.end,
                                                 self.duration,
                                                 self.type])) + ")"

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def _type_from_name(name):
        if name[-3:] == '***':
            return Activity.Type.IGNORED
        if name[-2:] == '**':
            return Activity.Type.BREAK
        return Activity.Type.WORK
