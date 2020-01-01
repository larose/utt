from utt.api import _v1


class FooHandler:
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        print("foo")


class FooCommand:
    NAME = "foo"
    DESCRIPTION = "Foo"

    Handler = FooHandler

    @staticmethod
    def add_args(parser):
        pass


_v1.add_command(FooCommand)
