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

from .axis_direction_component_child import axis_direction_component_child

class direction_component_of_rotation_axis(ListObject[axis_direction_component_child]):
    """
    'direction_component_of_rotation_axis' child.
    """

    fluent_name = "direction-component-of-rotation-axis"

    child_object_type: axis_direction_component_child = axis_direction_component_child
    """
    child_object_type of direction_component_of_rotation_axis.
    """
