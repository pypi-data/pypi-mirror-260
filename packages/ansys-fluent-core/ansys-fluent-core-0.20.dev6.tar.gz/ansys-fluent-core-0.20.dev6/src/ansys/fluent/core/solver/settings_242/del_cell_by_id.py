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

from .cellids import cellids as cellids_cls
class del_cell_by_id(Command):
    """
    Delete cells based on cell ids.
    
    Parameters
    ----------
        cellids : typing.List[int]
            Provide a list of cell ids.
    
    """

    fluent_name = "del-cell-by-id"

    argument_names = \
        ['cellids']

    _child_classes = dict(
        cellids=cellids_cls,
    )

