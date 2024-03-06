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

from .change_type import change_type as change_type_cls
from .porous_jump_child import porous_jump_child

class porous_jump(NamedObject[porous_jump_child], _CreatableNamedObjectMixin[porous_jump_child]):
    """
    'porous_jump' child.
    """

    fluent_name = "porous-jump"

    command_names = \
        ['change_type']

    _child_classes = dict(
        change_type=change_type_cls,
    )

    child_object_type: porous_jump_child = porous_jump_child
    """
    child_object_type of porous_jump.
    """
