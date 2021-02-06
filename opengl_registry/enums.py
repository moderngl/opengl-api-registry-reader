from typing import List, Optional

from opengl_registry.group import Group


class Enums:
    """Group of enums in a range reserved for a vendor"""

    def __init__(
        self,
        *,
        namespace: str,
        group: Group = None,
        type: str,
        start: str = None,
        end: str = None,
        vendor: str = None,
        comment: str = None,
        group_name: str = None,
        entries: List["Enum"] = None
    ):
        """Initialize an enum group.

        This represents a reserved enum range normally reserved for a specific vendor.

        Keyword Args:
            namespace (str): Namespace for the range (Usually always ``GL``)
            start (str): Range start as a hex string
            end (str): Range end as a hex string
            vendor (str): The vendor this enum block as assigned to (ARB, MESA, NV, AMD, QCOM etc.)
            comment (str): Enum range comment from the spec
            group (Group): The ``Group`` this enum collection is related to
            group_name (str): The group name
            type (str): Enum type
        """
        self._namespace = namespace
        self._start = start
        self._end = end
        self._vendor = vendor
        self._comment = comment
        self._group = group
        self._group_name = group_name
        self._type = type
        self._entries = entries or []

    @property
    def namespace(self) -> str:
        """str: Namespace for the range (Usually always ``GL``)"""
        return self._namespace

    @property
    def group(self) -> Optional[Group]:
        """Group: The group this enum range belongs to"""
        return self._group

    @group.setter
    def group(self, value: Group):
        self._group = value

    @property
    def type(self) -> str:
        """str: Enum type"""
        return self._type

    @property
    def start(self) -> Optional[str]:
        """str: Range start as a hex string"""
        return self._start

    @property
    def end(self) -> Optional[str]:
        """str: Range end as a hex string"""
        return self._end

    @property
    def vendor(self) -> Optional[str]:
        """str: The vendor this enum block as assigned to (ARB, MESA, NV, AMD, QCOM etc.)"""
        return self._vendor

    @property
    def group_name(self) -> Optional[str]:
        return self._group_name

    @property
    def comment(self) -> Optional[str]:
        """str: Enum range comment from the spec"""
        return self._comment

    @property
    def entires(self) -> List["Enum"]:
        return self._entries

    def __str__(self) -> str:
        return "<Enums {} - {}>".format(self._start, self._end)

    def __repr__(self) -> str:
        return str(self)


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
        self._range = None

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

    @property
    def range(self) -> Enums:
        """Enums: The enum range this enum belongs to"""
        return self._range

    @range.setter
    def range(self, value: Enums):
        self._range = value

    def __str__(self) -> str:
        return "<Enum {} [{}]>".format(self._name, self._value)

    def __repr__(self) -> str:
        return str(self)
