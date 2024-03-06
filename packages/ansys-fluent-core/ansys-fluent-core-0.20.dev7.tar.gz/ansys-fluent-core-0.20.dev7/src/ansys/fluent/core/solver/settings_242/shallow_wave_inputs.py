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
from .shallow_wave_inputs_child import shallow_wave_inputs_child

class shallow_wave_inputs(ListObject[shallow_wave_inputs_child]):
    """
    Shallow Wave Inputs.
    """

    fluent_name = "shallow-wave-inputs"

    command_names = \
        ['list_properties', 'resize']

    _child_classes = dict(
        list_properties=list_properties_cls,
        resize=resize_cls,
    )

    child_object_type: shallow_wave_inputs_child = shallow_wave_inputs_child
    """
    child_object_type of shallow_wave_inputs.
    """
