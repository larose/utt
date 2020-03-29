from ...components.output import Output
from .. import formatter
from ..common import print_dicts
from .model import ActivitiesModel


class ActivitiesView:
    def __init__(self, model: ActivitiesModel):
        self._model = model

    def render(self, output: Output) -> None:
        print(file=output)
        print(formatter.title("Activities"), file=output)
        print(file=output)

        print_dicts(self._model.names_work, output)

        print(file=output)

        print_dicts(self._model.names_break, output)
