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
from .set_damping_strengths_child import set_damping_strengths_child

class partition_origin_vector(ListObject[set_damping_strengths_child]):
    """
    'partition_origin_vector' child.
    """

    fluent_name = "partition-origin-vector"

    command_names = \
        ['list_properties']

    _child_classes = dict(
        list_properties=list_properties_cls,
    )

    child_object_type: set_damping_strengths_child = set_damping_strengths_child
    """
    child_object_type of partition_origin_vector.
    """
