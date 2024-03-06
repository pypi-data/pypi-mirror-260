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
from .pressure_far_field_child import pressure_far_field_child

class pressure_far_field(NamedObject[pressure_far_field_child], _NonCreatableNamedObjectMixin[pressure_far_field_child]):
    """
    'pressure_far_field' child.
    """

    fluent_name = "pressure-far-field"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    _child_classes = dict(
        list=list_cls,
        list_properties=list_properties_cls,
        duplicate=duplicate_cls,
    )

    child_object_type: pressure_far_field_child = pressure_far_field_child
    """
    child_object_type of pressure_far_field.
    """
