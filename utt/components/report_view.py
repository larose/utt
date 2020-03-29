from abc import ABC, abstractmethod

from ..components.output import Output


class ReportView(ABC):
    @abstractmethod
    def render(self, output: Output) -> None:
        raise NotImplementedError()
