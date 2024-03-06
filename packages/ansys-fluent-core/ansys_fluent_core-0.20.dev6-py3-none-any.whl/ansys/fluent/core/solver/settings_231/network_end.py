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

from .network_end_child import network_end_child

class network_end(NamedObject[network_end_child], _NonCreatableNamedObjectMixin[network_end_child]):
    """
    'network_end' child.
    """

    fluent_name = "network-end"

    child_object_type: network_end_child = network_end_child
    """
    child_object_type of network_end.
    """
