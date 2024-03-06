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

from .child_object_type_child_1 import child_object_type_child

class reference_frame_axis_direction(ListObject[child_object_type_child]):
    """
    'reference_frame_axis_direction' child.
    """

    fluent_name = "reference-frame-axis-direction"

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of reference_frame_axis_direction.
    """
