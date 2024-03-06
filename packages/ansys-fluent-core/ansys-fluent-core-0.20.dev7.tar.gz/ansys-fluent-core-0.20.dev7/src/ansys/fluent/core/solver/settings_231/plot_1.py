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

from .x_axis_function import x_axis_function as x_axis_function_cls
from .enabled_2 import enabled as enabled_cls
class plot(Group):
    """
    'plot' child.
    """

    fluent_name = "plot"

    child_names = \
        ['x_axis_function', 'enabled']

    _child_classes = dict(
        x_axis_function=x_axis_function_cls,
        enabled=enabled_cls,
    )

