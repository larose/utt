import copy

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
        return "Activity(" + ", ".join(
            map(str, [
                self.name, self.start, self.end, self.duration, self.type
            ])) + ")"

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def _type_from_name(name):
        if name[-3:] == '***':
            return Activity.Type.IGNORED
        if name[-2:] == '**':
            return Activity.Type.BREAK
        return Activity.Type.WORK

    def clip(self, start=None, end=None):
        """ Return a new Activity with the start and end time clipped to the
        given range.

        Parameters
        ----------
        start : datetime.datetime
            Start time to clip to (inclusive).
        end : datetime.datetime
            End time to clip to (inclusive).

        Returns
        -------
        new_activity : Activity
        """
        new_activity = copy.copy(self)
        if start is not None:
            new_activity.start = min(new_activity.end,
                                     max(new_activity.start, start))
        if end is not None:
            new_activity.end = max(new_activity.start,
                                   min(new_activity.end, end))
        new_activity.duration = new_activity.end - new_activity.start
        return new_activity
