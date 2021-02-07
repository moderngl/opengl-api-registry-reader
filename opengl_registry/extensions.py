from typing import List

class Extension:
    """An OpenGL extensions containins enum and command names to add"""

    def __init__(self, *, name: str, supported: str, enums: List[str], commands: List[str]):
        self._name = name
        self._supported = supported
        self._enums = enums
        self._commands = commands
    
    def __repr__(self) -> str:
        return "<Extension {} [{}]: enums={} commands={}".format(
            self._name, self._supported, self._enums, self._commands
        )

    @property
    def name(self) -> str:
        return self._name

    @property
    def enums(self) -> List[str]:
        """List if enum names to include"""
        return self._enums

    @property
    def commands(self) -> List[str]:
        """List of command names to include"""
        return self._commands
