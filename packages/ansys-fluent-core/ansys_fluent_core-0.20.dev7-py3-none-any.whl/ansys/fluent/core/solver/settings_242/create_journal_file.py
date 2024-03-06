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

from .rom_type_2 import rom_type as rom_type_cls
class create_journal_file(Command):
    """
    Create journal file.
    
    Parameters
    ----------
        rom_type : int
            ROM type in the ROM simulation.
    
    """

    fluent_name = "create-journal-file"

    argument_names = \
        ['rom_type']

    _child_classes = dict(
        rom_type=rom_type_cls,
    )

