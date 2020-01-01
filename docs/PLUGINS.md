# How to write a utt plugin

utt plugins allow to add new commands to utt. For example, `$ utt
<your new command>`.

A utt plugin is simply a [namespace
package](https://packaging.python.org/guides/packaging-namespace-packages/)
in the `utt.plugins` namespace.

You can find an [example plugin](../test/integration/utt_foo_plugin)
in the tests:

```
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
```

`_v1` is the current API version. It's prefixed with `_` to indicate
that the version (`v1) is not stable yet. Once it is be stable, the
`_` will be removed.


Note that you the handler's constructor can receive
arguments. Example:
[../utt/plugins/stretch.py](../utt/plugins/stretch.py):

```
class StretchHandler:
    # pylint: disable=too-many-arguments
    def __init__(self, args, now, add_entry, entries, timezone_config):
        self._args = args
        self._now = now
        self._add_entry = add_entry
        self._entries = entries
        self._timezone_config = timezone_config
```

See the [`create_container`](../utt/container.py) function for the
list of all possible arguments. Note that these arguments are not yet
versioned are therefore are subject to change.


## Tips

Never import "private" utt modules in your plugins. Only import
packages under the `utt.api` package.
