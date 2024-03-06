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
from .pressure_outlet_child import pressure_outlet_child

class pressure_outlet(NamedObject[pressure_outlet_child], _NonCreatableNamedObjectMixin[pressure_outlet_child]):
    """
    'pressure_outlet' child.
    """

    fluent_name = "pressure-outlet"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    _child_classes = dict(
        list=list_cls,
        list_properties=list_properties_cls,
        duplicate=duplicate_cls,
    )

    child_object_type: pressure_outlet_child = pressure_outlet_child
    """
    child_object_type of pressure_outlet.
    """
