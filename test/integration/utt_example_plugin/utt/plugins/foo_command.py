from utt.api import _v1


class FooHandler:
    def __init__(self, now: _v1.Now, output: _v1.Output):
        self._now = now
        self._output = output

    def __call__(self):
        print(f"Now: {self._now}", file=self._output)


foo_command = _v1.Command(name="foo", description="Foo", handler_class=FooHandler, add_args=lambda p: None)


_v1.register_command(foo_command)
