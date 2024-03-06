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
class plot(Group):
    """
    'plot' child.
    """

    fluent_name = "plot"

    child_names = \
        ['xy_plot', 'histogram', 'cumulative_plot']

    _child_classes = dict(
        xy_plot=xy_plot_cls,
        histogram=histogram_cls,
        cumulative_plot=cumulative_plot_cls,
    )

