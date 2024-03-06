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
from .network_end_child import network_end_child

class network_end(NamedObject[network_end_child], _CreatableNamedObjectMixin[network_end_child]):
    """
    'network_end' child.
    """

    fluent_name = "network-end"

    command_names = \
        ['change_type']

    _child_classes = dict(
        change_type=change_type_cls,
    )

    child_object_type: network_end_child = network_end_child
    """
    child_object_type of network_end.
    """
