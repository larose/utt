from datetime import timedelta

from ...components.output import Output
from .. import formatter
from .model import ProjectSummaryModel


class ProjectSummaryView:
    def __init__(self, model: ProjectSummaryModel, show_perc: bool = False):
        self._model = model
        self._show_perc = show_perc

    def render(self, output: Output) -> None:
        print(file=output)
        print(formatter.title("Project Summary"), file=output)
        print(file=output)

        max_project_length = max((len(p["project"]) for p in self._model.projects), default=0)
        
        total_seconds = sum((p["duration_obj"] for p in self._model.projects), timedelta()).total_seconds()
        if self._model.current_activity:
            total_seconds += self._model.current_activity["duration_obj"].total_seconds()

        for project in self._model.projects:
            duration_str = project['duration']
            if self._show_perc and total_seconds > 0:
                perc = (project['duration_obj'].total_seconds() / total_seconds) * 100
                duration_str = f"{duration_str} ({perc:5.1f}%)"
            print(f"{project['project']:<{max_project_length}}: {duration_str}", file=output)

        if self._model.current_activity:
            name = self._model.current_activity["name"]
            duration_str = self._model.current_activity["duration"]
            if self._show_perc and total_seconds > 0:
                perc = (self._model.current_activity["duration_obj"].total_seconds() / total_seconds) * 100
                duration_str = f"{duration_str} ({perc:5.1f}%)"
            print(f"{name:<{max_project_length}}: {duration_str}", file=output)

        print(file=output)
        total_str = self._model.total_duration
        if self._show_perc:
            total_str = f"{total_str} (100.0%)"
        print(f"{'Total':<{max_project_length}}: {total_str}", file=output)

        print(file=output)
