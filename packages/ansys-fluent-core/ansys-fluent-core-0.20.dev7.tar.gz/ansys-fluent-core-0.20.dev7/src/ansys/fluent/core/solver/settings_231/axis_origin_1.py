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

class axis_origin(ListObject[child_object_type_child]):
    """
    'axis_origin' child.
    """

    fluent_name = "axis-origin"

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of axis_origin.
    """
