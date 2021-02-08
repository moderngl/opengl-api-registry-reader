from typing import Dict, List, NoReturn
import logging

from opengl_registry.gltype import GlType
from opengl_registry.enums import Enum
from opengl_registry.commands import Command
from opengl_registry.features import Feature
from opengl_registry.extensions import Extension

logger = logging.getLogger(__name__)


class Registry:
    """A collection of all registry information"""

    def __init__(
        self,
        *,
        types: List[GlType] = None,
        enums: Dict[str, Enum] = None,
        commands: Dict[str, Command] = None,
        features: List[Feature] = None,
        extensions: Dict[str, Extension]  = None,
    ):
        """Initialize the registry.

        Keyword Args:
            types (List[Type]): List of types
            groups (List[Group]): List of groups
        """
        self._types = types or []
        self._enums: Dict[str, Enum] = enums or {}
        self._commands: Dict[str, Command] = commands or {}
        self._features = features or []
        self._extensions: Dict[str, Extension] = extensions or {}

    def __repr__(self) -> str:
        return f"<Registry: enums={len(self._enums)}, commands={len(self._commands)} extensions={len(self._extensions)}>"

    @property
    def enums(self) -> Dict[str, Enum]:
        return self._enums

    @property
    def commands(self) -> Dict[str, Command]:
        return self._commands

    @property
    def features(self):
        return self._features

    @property
    def extensions(self) -> List[Extension]:
        return self._extensions

    @property
    def types(self) -> List[GlType]:
        """List[Type]: List of all types"""
        return self._types

    def get_enum(self, name: str):
        return self._enums.get(name)

    def add_enum(self, enum: Enum):
        self._enums[enum.name] = enum

    def remove_enum(self, name: str) -> bool:
        if name in self._enums:
            del self._enums[name]
            return True
        return False

    def get_command(self, name: str):
        return self._commands.get(name)

    def add_command(self, command: Command):
        self._commands[command.name] = command

    def remove_command(self, name: str) -> bool:
        if name in self._commands:
            del self._commands[name]
            return True
        return False

    def get_extension(self, name) -> Extension:
        """Get an extension by name"""
        if not name.startswith("GL_"):
            name = f"GL_{name}"

        return self._extensions[name]

    def get_profile(
        self, api: str = "gl", profile: str = "core", version: str = "3.3", extensions=List[str],
    ) -> "Registry":
        """Get a subset of the registry"""
        # Create the new registry
        registry = Registry(
            types=self._types,
        )

        for feature in self._features:
            # Skip features not belonging to the api
            if feature.api != api:
                continue

            if feature.number > version:
                continue

            # Add the required
            for details in feature.require:
                for name in details.enums:
                    enum = self.get_enum(name)
                    if enum:
                        registry.add_enum(enum)
                    else:
                        raise ValueError("Cannot add enum", name)

                for name in details.commands:
                    command = self.get_command(name)
                    command.requires = feature.number
                    if command:
                        registry.add_command(command)
                    else:
                        raise ValueError("Cannot add command", name)                        

            # Remove features
            if profile == "core":
                for details in feature.remove:
                    for name in details.enums:
                        if not registry.remove_enum(name):
                            raise ValueError("Cannot remove enum", name)

                    for name in details.commands:
                        if not registry.remove_command(name):
                            raise ValueError("Cannot remove command", name)

        # Add extensions
        for ext_name in extensions:
            ext = self.get_extension(ext_name)
            for name in ext.enums:
                registry.add_enum(self.get_enum(name))
            for name in ext.commands:
                registry.add_command(self.get_command(name))

        return registry
