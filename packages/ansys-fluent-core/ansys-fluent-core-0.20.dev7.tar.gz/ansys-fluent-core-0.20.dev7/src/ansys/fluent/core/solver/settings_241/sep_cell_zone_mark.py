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

from .cell_zone_name_1 import cell_zone_name as cell_zone_name_cls
from .register import register as register_cls
from .move_faces import move_faces as move_faces_cls
class sep_cell_zone_mark(Command):
    """
    Separate a cell zone based on cell marking.
    
    Parameters
    ----------
        cell_zone_name : str
            Enter a zone name.
        register : str
            'register' child.
        move_faces : bool
            'move_faces' child.
    
    """

    fluent_name = "sep-cell-zone-mark"

    argument_names = \
        ['cell_zone_name', 'register', 'move_faces']

    _child_classes = dict(
        cell_zone_name=cell_zone_name_cls,
        register=register_cls,
        move_faces=move_faces_cls,
    )

