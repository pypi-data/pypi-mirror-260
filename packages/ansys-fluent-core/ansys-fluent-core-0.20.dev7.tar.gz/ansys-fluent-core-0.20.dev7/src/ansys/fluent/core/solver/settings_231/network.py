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

from .network_child import network_child

class network(NamedObject[network_child], _NonCreatableNamedObjectMixin[network_child]):
    """
    'network' child.
    """

    fluent_name = "network"

    child_object_type: network_child = network_child
    """
    child_object_type of network.
    """
