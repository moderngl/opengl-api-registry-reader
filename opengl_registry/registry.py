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
        extensions: List[Extension]  = None,
    ):
        """Initialize the registry.

        Keyword Args:
            types (List[Type]): List of types
            groups (List[Group]): List of groups
        """
        self._types = types or []
        self._enums: Dict[str, Enum] = enums or [],
        self._commands: Dict[str, Command] = commands or []
        self._features = features or []
        self._extensions = extensions or []

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

    def get_profile(
        self, api: str = "gl", profile: str = "core", version: str = "3.3", extensions=None
    ):
        """Get a subset of the registry"""
        registry = Registry(
            types=self._types,
        )

        for feature in self._features:
            # Skip features not belonging to the api
            if feature.api != api:
                continue

            print(feature)
            # for require in feature.require:
            #     print("require", require)
            
            for remove in feature.remove:
                print("remove", remove)
