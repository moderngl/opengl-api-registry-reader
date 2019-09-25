from typing import List


class CommandParam:
    """Command parameter"""

    def __init__(self, name=None, value=None, ptype=None, group=None, length=None, alias=None):
        self._name = name
        self._value = value
        self._ptype = ptype
        self._group = group
        self._length = length
        self._alias = alias

    @property
    def name(self):
        """str: parameter name"""
        return self._name

    @property
    def value(self) -> str:
        """str: full declaration string"""
        return self._name

    @property
    def ptype(self) -> str:
        """str: parameter type"""
        return self._ptype

    @property
    def group(self) -> str:
        """str: group name"""
        return self._group

    @property
    def alias(self) -> str:
        """str: command alias.
        Usually a shorter name witout extension suffix.
        """
        return self._alias

    @property
    def length(self):
        """str: data length"""
        return self._length


class Command:
    """GL functions"""

    def __init__(self, proto=None, name=None, params=None, glx=None):
        self._proto = proto
        self._name = name
        self._params = params or []
        self._glx = glx

    @property
    def proto(self) -> str:
        return self._name

    @proto.setter
    def proto(self, value):
        self._name = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def params(self) -> str:
        return self._params

    @property
    def glx(self) -> dict:
        return self._glx

    @glx.setter
    def glx(self, value):
        self._glx = value

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "<Command {} {}".format(self._name, [p.name for p in self._params])

class Commands:
    """A group of commands"""

    def __init__(self, namespace='GL', entires=None):
        self._namespace = namespace
        self._entries = entires or []

    @property
    def namespace(self) -> str:
        return self._namespace

    @property
    def entries(self) -> List[Command]:
        """List[Command]: all commands"""
        return self._entries
