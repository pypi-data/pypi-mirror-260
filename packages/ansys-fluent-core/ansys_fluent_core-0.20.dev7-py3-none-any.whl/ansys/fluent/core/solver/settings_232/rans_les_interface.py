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
from .rans_les_interface_child import rans_les_interface_child

class rans_les_interface(NamedObject[rans_les_interface_child], _NonCreatableNamedObjectMixin[rans_les_interface_child]):
    """
    'rans_les_interface' child.
    """

    fluent_name = "rans-les-interface"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    _child_classes = dict(
        list=list_cls,
        list_properties=list_properties_cls,
        duplicate=duplicate_cls,
    )

    child_object_type: rans_les_interface_child = rans_les_interface_child
    """
    child_object_type of rans_les_interface.
    """
