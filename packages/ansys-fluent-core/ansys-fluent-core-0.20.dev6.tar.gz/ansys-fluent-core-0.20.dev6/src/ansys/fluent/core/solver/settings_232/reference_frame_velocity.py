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

from .list_properties_1 import list_properties as list_properties_cls
from .child_object_type_child_1 import child_object_type_child

class reference_frame_velocity(ListObject[child_object_type_child]):
    """
    'reference_frame_velocity' child.
    """

    fluent_name = "reference-frame-velocity"

    command_names = \
        ['list_properties']

    _child_classes = dict(
        list_properties=list_properties_cls,
    )

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of reference_frame_velocity.
    """
