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

from .list import list as list_cls
from .list_properties import list_properties as list_properties_cls
from .duplicate import duplicate as duplicate_cls
from .exhaust_fan_child import exhaust_fan_child

class exhaust_fan(NamedObject[exhaust_fan_child], _NonCreatableNamedObjectMixin[exhaust_fan_child]):
    """
    'exhaust_fan' child.
    """

    fluent_name = "exhaust-fan"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    _child_classes = dict(
        list=list_cls,
        list_properties=list_properties_cls,
        duplicate=duplicate_cls,
    )

    child_object_type: exhaust_fan_child = exhaust_fan_child
    """
    child_object_type of exhaust_fan.
    """
