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
from .turbo_interface_child import turbo_interface_child

class turbo_interface(NamedObject[turbo_interface_child], _CreatableNamedObjectMixin[turbo_interface_child]):
    """
    'turbo_interface' child.
    """

    fluent_name = "turbo-interface"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    _child_classes = dict(
        list=list_cls,
        list_properties=list_properties_cls,
        duplicate=duplicate_cls,
    )

    child_object_type: turbo_interface_child = turbo_interface_child
    """
    child_object_type of turbo_interface.
    """
