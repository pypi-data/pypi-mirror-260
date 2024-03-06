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

from .zone_1 import zone as zone_cls
from .y_axis_function_1 import y_axis_function as y_axis_function_cls
from .x_axis_function_1 import x_axis_function as x_axis_function_cls
from .axes import axes as axes_cls
from .curves import curves as curves_cls
from .plot_10 import plot as plot_cls
class interpolated_data(Group):
    """
    Display interpolated data.
    """

    fluent_name = "interpolated-data"

    child_names = \
        ['zone', 'y_axis_function', 'x_axis_function', 'axes', 'curves']

    command_names = \
        ['plot']

    _child_classes = dict(
        zone=zone_cls,
        y_axis_function=y_axis_function_cls,
        x_axis_function=x_axis_function_cls,
        axes=axes_cls,
        curves=curves_cls,
        plot=plot_cls,
    )

