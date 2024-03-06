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
from .piecewise_linear_child import piecewise_linear_child

class piecewise_linear(ListObject[piecewise_linear_child]):
    """
    Specify data-points for piecewise linear interpolation.
    """

    fluent_name = "piecewise-linear"

    command_names = \
        ['list_properties', 'resize']

    _child_classes = dict(
        list_properties=list_properties_cls,
        resize=resize_cls,
    )

    child_object_type: piecewise_linear_child = piecewise_linear_child
    """
    child_object_type of piecewise_linear.
    """
