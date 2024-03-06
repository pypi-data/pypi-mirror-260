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

from .profile_5 import profile as profile_cls
from .y_axis_function_1 import y_axis_function as y_axis_function_cls
from .x_axis_function_1 import x_axis_function as x_axis_function_cls
from .axes import axes as axes_cls
from .curves import curves as curves_cls
from .plot_9 import plot as plot_cls
class profile_data(Group):
    """
    Display profile data.
    """

    fluent_name = "profile-data"

    child_names = \
        ['profile', 'y_axis_function', 'x_axis_function', 'axes', 'curves']

    command_names = \
        ['plot']

    _child_classes = dict(
        profile=profile_cls,
        y_axis_function=y_axis_function_cls,
        x_axis_function=x_axis_function_cls,
        axes=axes_cls,
        curves=curves_cls,
        plot=plot_cls,
    )

