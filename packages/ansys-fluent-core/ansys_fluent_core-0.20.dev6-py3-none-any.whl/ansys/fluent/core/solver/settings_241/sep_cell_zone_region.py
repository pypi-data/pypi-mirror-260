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
from .move_cells import move_cells as move_cells_cls
class sep_cell_zone_region(Command):
    """
    Separate a cell zone based on contiguous regions.
    
    Parameters
    ----------
        cell_zone_name : str
            Enter a zone name.
        move_cells : bool
            'move_cells' child.
    
    """

    fluent_name = "sep-cell-zone-region"

    argument_names = \
        ['cell_zone_name', 'move_cells']

    _child_classes = dict(
        cell_zone_name=cell_zone_name_cls,
        move_cells=move_cells_cls,
    )

