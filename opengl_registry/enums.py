from typing import List, Optional


class Enum:
    """Container for GL enum info"""

    def __init__(self, *, name: str, value: str, alias: str, comment=None):
        """Initialize an enum instance.

        Args:
            name (str): Name of the enum
            value (str): Enum value (hex number as string)
        Keyword Args:
            comment (str): Enum comment
        """
        self._name = name
        self._value = value
        self._alias = alias
        self._comment = comment

    @property
    def name(self) -> str:
        """str: Name of the enum"""
        return self._name

    @property
    def comment(self) -> str:
        """str: Enum comment"""
        return self._comment

    @property
    def value(self) -> str:
        """str: Enum value (hex number as string)"""
        return self._value

    @property
    def value_int(self) -> int:
        """int: Enum value as as int"""
        return int(self._value, base=16)

    def __lt__(self, other):
        return self.value_int < other.value_int

    def __str__(self) -> str:
        return "<Enum {} [{}]>".format(self._name, self._value)

    def __repr__(self) -> str:
        return str(self)
