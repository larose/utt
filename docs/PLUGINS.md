# How to write a utt plugin

utt plugins allow to add new commands to utt. For example, `$ utt
foo`, where `foo` is a new command.

A utt plugin is simply a [namespace
package](https://packaging.python.org/guides/packaging-namespace-packages/)
in the `utt.plugins`.

You can find an [example plugin](../test/integration/utt_foo_plugin)
in the tests:

```
from utt.api import _v1


class FooHandler:
    def __init__(self, now: _v1.Now, output: _v1.Output):
        self._now = now
        self._output = output

    def __call__(self):
        print(f"Now: {self._now}", file=self._output)


foo_command = _v1.Command(name="foo", description="Foo", handler_class=FooHandler, add_args=lambda p: None)


_v1.register_command(foo_command)
```

This plugins first imports utt's api:

```
from utt.api import _v1
```

Note that `_v1` is the latest utt's api version. It's prefixed with
`_` to indicate that the version (`v1`) is not stable yet. `_` will be
removed once it is be stable.

Then the plugin declares a command handler and a command:

```
class FooHandler:
    ...

foo_command = _v1.Command(name="foo", description="Foo", handler_class=FooHandler, add_args=lambda p: None)
    ...
```

The handler can receive arguments that are injected by utt:

```
class FooHandler:
    def __init__(self, now: _v1.Now, output: _v1.Output):
        ...
```

Consult [`../utt/api/_v1/__init__.py`](../utt/api/_v1/__init__.py) to
see the list of available types that can be injected.

Finally, the plugin registers the new command to utt:

```
_v1.register_command(foo_command)
```


## Best practices

All symbols exported in
[`../utt/api/_v1/__init__.py`](../utt/api/_v1/__init__.py) are part of
the public api and are safe to use. (However, note that `_v1` is still
in development and we may introduce breaking changes until it becomes
stable.)

Therefore, anything not exported in
[`../utt/api/_v1/__init__.py`](../utt/api/_v1/__init__.py) is not part
of utt's api and should not be imported in your plugin.
