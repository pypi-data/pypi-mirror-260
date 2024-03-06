#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import (
    _ChildNamedObjectAccessorMixin,
    _CreatableNamedObjectMixin,
    _NonCreatableNamedObjectMixin,
    _HasAllowedValuesMixin,
    _InputFile,
    _OutputFile,
    _InOutFile,
)

from .rom_data_creator_tool import rom_data_creator_tool as rom_data_creator_tool_cls
from .lti_rom_generation import lti_rom_generation as lti_rom_generation_cls
class rom_tool_kit(Group):
    """
    ROM tool kits.
    """

    fluent_name = "rom-tool-kit"

    child_names = \
        ['rom_data_creator_tool', 'lti_rom_generation']

    _child_classes = dict(
        rom_data_creator_tool=rom_data_creator_tool_cls,
        lti_rom_generation=lti_rom_generation_cls,
    )

