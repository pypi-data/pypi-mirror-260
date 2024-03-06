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
from .wave_list_shallow_child import wave_list_shallow_child

class wave_list_shallow(ListObject[wave_list_shallow_child]):
    """
    'wave_list_shallow' child.
    """

    fluent_name = "wave-list-shallow"

    command_names = \
        ['list_properties']

    _child_classes = dict(
        list_properties=list_properties_cls,
    )

    child_object_type: wave_list_shallow_child = wave_list_shallow_child
    """
    child_object_type of wave_list_shallow.
    """
