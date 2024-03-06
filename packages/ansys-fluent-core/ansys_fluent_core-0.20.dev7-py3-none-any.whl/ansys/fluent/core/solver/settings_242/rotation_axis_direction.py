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

from .list_properties import list_properties as list_properties_cls
from .resize import resize as resize_cls
from .cone_axis_vector_child import cone_axis_vector_child

class rotation_axis_direction(ListObject[cone_axis_vector_child]):
    """
    Set rotation axis direction components.
    """

    fluent_name = "rotation-axis-direction"

    command_names = \
        ['list_properties', 'resize']

    _child_classes = dict(
        list_properties=list_properties_cls,
        resize=resize_cls,
    )

    child_object_type: cone_axis_vector_child = cone_axis_vector_child
    """
    child_object_type of rotation_axis_direction.
    """
