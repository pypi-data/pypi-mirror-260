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

from .child_object_type_child import child_object_type_child

class solid_motion_velocity_components(ListObject[child_object_type_child]):
    """
    'solid_motion_velocity_components' child.
    """

    fluent_name = "solid-motion-velocity-components"

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of solid_motion_velocity_components.
    """
