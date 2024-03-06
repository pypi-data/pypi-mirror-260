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

from .list_properties import list_properties as list_properties_cls
from .resize import resize as resize_cls
from .wave_group_inputs_child import wave_group_inputs_child

class wave_group_inputs(ListObject[wave_group_inputs_child]):
    """
    Wave Group Inputs.
    """

    fluent_name = "wave-group-inputs"

    command_names = \
        ['list_properties', 'resize']

    _child_classes = dict(
        list_properties=list_properties_cls,
        resize=resize_cls,
    )

    child_object_type: wave_group_inputs_child = wave_group_inputs_child
    """
    child_object_type of wave_group_inputs.
    """
