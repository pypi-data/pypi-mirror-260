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

from .cell_registers_child import cell_registers_child

class cell_registers(NamedObject[cell_registers_child], _CreatableNamedObjectMixin[cell_registers_child]):
    """
    'cell_registers' child.
    """

    fluent_name = "cell-registers"

    child_object_type: cell_registers_child = cell_registers_child
    """
    child_object_type of cell_registers.
    """
