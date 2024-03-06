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

from .cell_zone_list import cell_zone_list as cell_zone_list_cls
class activate_cell_zone(Command):
    """
    Activate a cell thread.
    
    Parameters
    ----------
        cell_zone_list : typing.List[str]
            'cell_zone_list' child.
    
    """

    fluent_name = "activate-cell-zone"

    argument_names = \
        ['cell_zone_list']

    _child_classes = dict(
        cell_zone_list=cell_zone_list_cls,
    )

