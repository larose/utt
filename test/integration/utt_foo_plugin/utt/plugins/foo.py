from utt.api import _v1


class FooHandler:
    def __init__(self, now: _v1.Now, output: _v1.Output):
        self._now = now
        self._output = output

    def __call__(self, *args, **kwargs):
        print(f"Now: {self._now}", file=self._output)


class FooCommand:
    NAME = "foo"
    DESCRIPTION = "Foo"

    Handler = FooHandler

    @staticmethod
    def add_args(parser):
        pass


_v1.add_command(FooCommand)
