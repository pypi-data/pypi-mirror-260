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
from .outlet_vent_child import outlet_vent_child

class outlet_vent(NamedObject[outlet_vent_child], _NonCreatableNamedObjectMixin[outlet_vent_child]):
    """
    'outlet_vent' child.
    """

    fluent_name = "outlet-vent"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    _child_classes = dict(
        list=list_cls,
        list_properties=list_properties_cls,
        duplicate=duplicate_cls,
    )

    child_object_type: outlet_vent_child = outlet_vent_child
    """
    child_object_type of outlet_vent.
    """
