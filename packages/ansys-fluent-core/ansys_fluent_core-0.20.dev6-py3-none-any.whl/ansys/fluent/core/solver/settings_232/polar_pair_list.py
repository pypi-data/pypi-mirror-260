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
from .polar_pair_list_child import polar_pair_list_child

class polar_pair_list(ListObject[polar_pair_list_child]):
    """
    'polar_pair_list' child.
    """

    fluent_name = "polar-pair-list"

    command_names = \
        ['list_properties']

    _child_classes = dict(
        list_properties=list_properties_cls,
    )

    child_object_type: polar_pair_list_child = polar_pair_list_child
    """
    child_object_type of polar_pair_list.
    """
