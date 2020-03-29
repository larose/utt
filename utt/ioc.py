import inspect
from abc import ABC, abstractmethod
from typing import Any, List, Type


class FactorySpec(ABC):
    @abstractmethod
    def arg_names(self) -> List[str]:
        raise NotImplementedError()

    @abstractmethod
    def spec(self):
        raise NotImplementedError()

    @abstractmethod
    def instantiate(self, args):
        raise NotImplementedError()


class ClassFactorySpec(FactorySpec):
    def __init__(self, cls):
        self._cls = cls

    def arg_names(self):
        return inspect.getfullargspec(self._cls.__init__).args[1:]

    def spec(self):
        return inspect.getfullargspec(self._cls.__init__)

    def instantiate(self, args):
        return self._cls(*args)


class FunctionFactorySpec(FactorySpec):
    def __init__(self, fn):
        self._fn = fn

    def arg_names(self):
        return inspect.getfullargspec(self._fn).args

    def spec(self):
        return inspect.getfullargspec(self._fn)

    def instantiate(self, args):
        return self._fn(*args)


class Factory:
    def __init__(self, factory_spec: FactorySpec):
        self._factory_spec = factory_spec
        self._called = False

    def _create(self, values):
        spec = self._factory_spec.spec()

        annotations = spec.annotations

        args = []
        for arg_name in self._factory_spec.arg_names():
            arg_type = annotations[arg_name]
            value = values[arg_type](values)
            args.append(value)

        return self._factory_spec.instantiate(args)

    def __call__(self, values):
        if not self._called:
            self._cached_value = self._create(values)
            self._called = True

        return self._cached_value


class Value:
    def __init__(self, value):
        self._value = value

    def __call__(self, values):
        return self._value


class Container:
    def __init__(self):
        self._values = {}

    def __setitem__(self, key: Type, value: Any):
        if inspect.isclass(value):
            self._values[key] = Factory(ClassFactorySpec(value))
        elif inspect.isfunction(value) or inspect.ismethod(value):
            self._values[key] = Factory(FunctionFactorySpec(value))
        else:
            self._values[key] = Value(value)

    def __getitem__(self, key):
        return self._values[key](self._values)
