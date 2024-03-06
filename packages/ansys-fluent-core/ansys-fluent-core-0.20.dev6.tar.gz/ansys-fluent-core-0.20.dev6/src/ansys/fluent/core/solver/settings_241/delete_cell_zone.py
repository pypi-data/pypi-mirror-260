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

from .cell_zones_2 import cell_zones as cell_zones_cls
class delete_cell_zone(Command):
    """
    Delete a cell thread.
    
    Parameters
    ----------
        cell_zones : typing.List[str]
            Delete a cell zone.
    
    """

    fluent_name = "delete-cell-zone"

    argument_names = \
        ['cell_zones']

    _child_classes = dict(
        cell_zones=cell_zones_cls,
    )

