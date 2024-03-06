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

from .axis_direction_child import axis_direction_child

class rotation_axis_origin(ListObject[axis_direction_child]):
    """
    'rotation_axis_origin' child.
    """

    fluent_name = "rotation-axis-origin"

    child_object_type: axis_direction_child = axis_direction_child
    """
    child_object_type of rotation_axis_origin.
    """
