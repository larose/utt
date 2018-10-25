import inspect


class Class:
    def __init__(self, cls):
        self._called = False
        self._cls = cls
        self._cached_value = None

    def __call__(self, values):
        if not self._called:
            arg_names = inspect.getargspec(self._cls.__init__).args  # pylint: disable=deprecated-method

            args = []
            for name in arg_names[1:]:
                value = values[name](values)
                args.append(value)

            self._cached_value = self._cls(*args)
            self._called = True

        return self._cached_value


class Function:
    def __init__(self, fn):
        self._called = False
        self._fn = fn
        self._cached_value = None

    def __call__(self, values):
        if not self._called:
            arg_names = inspect.getargspec(self._fn).args  # pylint: disable=deprecated-method

            args = []
            for name in arg_names:
                value = values[name](values)
                args.append(value)

            self._cached_value = self._fn(*args)
            self._called = True

        return self._cached_value


class Value:
    def __init__(self, value):
        self._value = value

    def __call__(self, values):
        return self._value


# pylint: disable=too-many-instance-attributes,useless-object-inheritance
class Container(object):
    def __init__(self):
        super(Container, self).__setattr__('_values', {})

    def __setattr__(self, key, value):
        if inspect.isclass(value):
            self._values[key] = Class(value)
        elif inspect.isfunction(value) or inspect.ismethod(value):
            self._values[key] = Function(value)
        else:
            self._values[key] = Value(value)

    def __getattr__(self, key):
        return self._values[key](self._values)
