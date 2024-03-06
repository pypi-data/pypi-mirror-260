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

from .name_1 import name as name_cls
from .python_name_1 import python_name_1 as python_name_1_cls
from .type_8 import type as type_cls
from .display_options import display_options as display_options_cls
class cell_registers_child(Group):
    """
    'child_object_type' of cell_registers.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'python_name_1', 'type', 'display_options']

    _child_classes = dict(
        name=name_cls,
        python_name_1=python_name_1_cls,
        type=type_cls,
        display_options=display_options_cls,
    )

