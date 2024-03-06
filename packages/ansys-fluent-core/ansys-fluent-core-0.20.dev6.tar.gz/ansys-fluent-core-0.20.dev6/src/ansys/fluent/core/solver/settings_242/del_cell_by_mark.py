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

from .register_1 import register as register_cls
class del_cell_by_mark(Command):
    """
    Delete cells based on a cell register.
    
    Parameters
    ----------
        register : str
            Provide the id or name of a register.
    
    """

    fluent_name = "del-cell-by-mark"

    argument_names = \
        ['register']

    _child_classes = dict(
        register=register_cls,
    )

