import logging
from io import StringIO
from opengl_registry.extensions import Extension
from typing import Dict, List
from xml.etree import ElementTree
import requests

# NOTE: Consider moving this to __init__ when finalized
from opengl_registry.registry import Registry
from opengl_registry.gltype import GlType
from opengl_registry.enums import Enum
from opengl_registry.commands import Command, CommandParam
from opengl_registry.features import Feature, FeatureDetails

# from opengl_registry.extensions import Extension

logger = logging.getLogger(__name__)


class RegistryReader:
    """Reads ``gl.xml`` file into a ``Registry`` structure
    that can easily be inspected.

    The reader instantiates data objects for every tag in the xml
    file. The created ``Registry`` is then responsible for making
    sense of the information.

    Example::

        # From a local file
        reader = RegistryReader.from_file('gl.xml')
        registry = reader.read()

        # From url. If no url parameter is passed in the last known url for this file is used.
        # Currently it resides on github in the KhronosGroup organization
        reader = RegistryReader.from_url()
        registry = reader.read()
    """

    #: The default URL for the ``gl.xml``` file
    DEFAULT_URL = "https://raw.githubusercontent.com/KhronosGroup/OpenGL-Registry/master/xml/gl.xml"

    #: The registry class. Can be replaced with a custom class
    registry_cls = Registry
    #: The GlType class. Can be replaced with a custom class
    type_cls = GlType
    #: The Enum class. Can be replaced with a custom class
    enum_cls = Enum

    def __init__(self, tree: ElementTree):
        """Initialize the reader.

        Currently we use `xml.etree.ElementTree` for parsing the
        registry information.

        Args:
            tree (ElementTree): The `ElementTree` instance
        """
        self._tree = tree

    @classmethod
    def from_file(cls, path: str) -> "RegistryReader":
        """Create a RegistryReader with a local gl.xml file"""
        logger.info("Reading registry file: '%s'", path)
        tree = ElementTree.parse(path)
        return cls(tree)

    @classmethod
    def from_url(cls, url: str = None) -> "RegistryReader":
        """Create a RegistryReader with a url to the gl.xml file"""
        url = url or cls.DEFAULT_URL
        logger.info("Reading registry file from url: '%s'", url)

        response = requests.get(url)
        if response.status_code != requests.codes.ok:
            response.raise_for_error()

        tree = ElementTree.parse(StringIO(response.text))
        return cls(tree)

    def read(self) -> Registry:
        """Reads the registry structure.

        Returns:
            Registry: The ``Registry`` instance
        """
        return self.registry_cls(
            types=self.read_types(),
            enums=self.read_enums(),
            commands=self.read_commands(),
            features=self.read_features(),
            extensions=self.read_extensions(),
        )

    def read_types(self) -> List[GlType]:
        """Read all GL type definitions

        Returns:
            List[GlType]: list of types
        """
        types = []

        for type_elem in self._tree.getroot().iter("type"):
            name = None
            try:
                name = next(type_elem.iter("name")).text
            except StopIteration:
                name = type_elem.get("name")

            types.append(
                self.type_cls(
                    name=name,
                    text="".join(type_elem.itertext()),
                    comment=type_elem.get("comment"),
                    requires=type_elem.get("requires"),
                )
            )

        return types

    ## Note: Khronos does not use the enum group information. Likely outdated.
    # def read_groups(self) -> List[Group]:
    #     """Reads all group nodes.

    #     Returns:
    #         List[Group]: list of groups
    #     """
    #     groups = []

    #     for groups_elem in self._tree.getroot().iter("group"):
    #         groups.append(
    #             self.group_cls(
    #                 groups_elem.attrib["name"],
    #                 entries={e.attrib["name"] for e in groups_elem.iter("enum")},
    #             )
    #         )

    #     return groups

    def read_enums(self) -> Dict[str, Enum]:
        """Reads all enums groups.

        Returns:
            List[Enums]: list of enums groups
        """
        enums = {}
        for enums_elem in self._tree.getroot().iter("enums"):
            enums.update({
                el.get("name"): Enum(
                    name=el.get("name"),
                    value=el.get("value"),
                    comment=el.get("comment"),
                    alias=el.get("alias"),
                )
                for el in enums_elem.iter("enum")
            })

        return enums

    def read_commands(self) -> Dict[str, Command]:
        """Reads all commands.

        Returns:
            List[Command]: list of commands
        """
        entries = {}
        commands_elem = next(self._tree.getroot().iter("commands"))
        for comm_elem in commands_elem.iter("command"):
            command = Command()

            for child in comm_elem:
                # A command should only have one proto tag
                if child.tag == "proto":
                    command.proto = "".join(child.itertext())
                    try:
                        ptype = next(child.iter("ptype"))
                        command.ptype = ptype.text
                    except StopIteration:
                        pass
                    command.name = next(child.iter("name")).text
                elif child.tag == "param":
                    name = next(child.iter("name")).text
                    value = "".join(child.itertext())
                    group = child.get("group")
                    length = child.get("len")
                    ptype = None
                    try:
                        ptype = next(child.iter("ptype")).text
                    except StopIteration:
                        pass
                    command.params.append(
                        CommandParam(
                            name=name,
                            value=value,
                            ptype=ptype,
                            group=group,
                            length=length,
                        )
                    )
                elif child.tag == "glx":
                    command.glx = {
                        "type": child.get("type"),
                        "opcode": child.get("opcode"),
                        "name": child.get("name"),
                        "comment": child.get("comment"),
                    }

                entries[command.name] = command

        return entries

    def read_features(self) -> List[Feature]:
        """Reads all features.

        Returns:
            List[Feature]: list of features
        """
        features = []
        for feature_elem in self._tree.iter("feature"):
            feature = Feature(
                api=feature_elem.get("api"),
                name=feature_elem.get("name"),
                number=feature_elem.get("number"),
            )
            features.append(feature)
            for details_elem in (
                *feature_elem.iter("require"),
                *feature_elem.iter("remove"),
            ):
                mode = details_elem.tag
                details = FeatureDetails(
                    mode,
                    profile=details_elem.get("profile"),
                    comment=details_elem.get("comment"),
                    enums=[t.get("name") for t in details_elem.iter("enum")],
                    commands=[t.get("name") for t in details_elem.iter("command")],
                    types=[t.get("name") for t in details_elem.iter("type")],
                )
                if mode == FeatureDetails.REQUIRE:
                    feature.require.append(details)
                elif mode == FeatureDetails.REMOVE:
                    feature.remove.append(details)
                else:
                    logger.warning("Unsupported mode: '%s'", mode)

        return features

    def read_extensions(self) -> Dict[str, Extension]:
        """Reads all extensions.

        Returns:
            List[Extension]: list of extensions
        """
        extensions = {}
        # NOTE: Extensions done have <remove>. We can safely iter
        for ext_elem in self._tree.iter("extension"):
            name = ext_elem.get("name")
            extensions[name] = Extension(
                name=name,
                supported=ext_elem.get("supported"),
                enums=[e.get("name") for e in ext_elem.iter("enum")],
                commands=[e.get("name") for e in ext_elem.iter("command")],
            )

        return extensions
