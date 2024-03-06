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
from .wall_child import wall_child

class wall(NamedObject[wall_child], _CreatableNamedObjectMixin[wall_child]):
    """
    'wall' child.
    """

    fluent_name = "wall"

    command_names = \
        ['change_type']

    _child_classes = dict(
        change_type=change_type_cls,
    )

    child_object_type: wall_child = wall_child
    """
    child_object_type of wall.
    """
