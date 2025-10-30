from ...components.output import Output
from .. import formatter
from .model import ProjectSummaryModel


class ProjectSummaryView:
    def __init__(self, model: ProjectSummaryModel):
        self._model = model

    def render(self, output: Output) -> None:
        print(file=output)
        print(formatter.title("Project Summary"), file=output)
        print(file=output)

        max_project_length = max((len(p["project"]) for p in self._model.projects), default=0)

        for project in self._model.projects:
            print(f"{project['project']:<{max_project_length}}: {project['duration']}", file=output)

        if self._model.current_activity:
            name = self._model.current_activity["name"]
            duration = self._model.current_activity["duration"]
            print(f"{name:<{max_project_length}}: {duration}", file=output)

        print(file=output)
        print(f"{'Total':<{max_project_length}}: {self._model.total_duration}", file=output)

        print(file=output)
