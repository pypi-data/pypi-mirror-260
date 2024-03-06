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

from .xy_plot import xy_plot as xy_plot_cls
from .histogram import histogram as histogram_cls
from .cumulative_plot import cumulative_plot as cumulative_plot_cls
from .solution_plot import solution_plot as solution_plot_cls
from .profile_data import profile_data as profile_data_cls
from .interpolated_data import interpolated_data as interpolated_data_cls
class plot(Group):
    """
    'plot' child.
    """

    fluent_name = "plot"

    child_names = \
        ['xy_plot', 'histogram', 'cumulative_plot', 'solution_plot',
         'profile_data', 'interpolated_data']

    _child_classes = dict(
        xy_plot=xy_plot_cls,
        histogram=histogram_cls,
        cumulative_plot=cumulative_plot_cls,
        solution_plot=solution_plot_cls,
        profile_data=profile_data_cls,
        interpolated_data=interpolated_data_cls,
    )

