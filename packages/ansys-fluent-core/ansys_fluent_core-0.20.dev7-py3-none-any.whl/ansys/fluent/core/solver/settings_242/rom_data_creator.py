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

from .rom_type_1 import rom_type as rom_type_cls
class rom_data_creator(Command):
    """
    ROM data creator.
    
    Parameters
    ----------
        rom_type : int
            ROM type in ROM-data creator.
    
    """

    fluent_name = "rom-data-creator"

    argument_names = \
        ['rom_type']

    _child_classes = dict(
        rom_type=rom_type_cls,
    )

