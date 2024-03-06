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

from .name_1 import name as name_cls
from .plot_window import plot_window as plot_window_cls
from .frequency import frequency as frequency_cls
from .flow_frequency import flow_frequency as flow_frequency_cls
from .frequency_of import frequency_of as frequency_of_cls
from .report_defs import report_defs as report_defs_cls
from .print_3 import print as print_cls
from .title import title as title_cls
from .x_label import x_label as x_label_cls
from .y_label import y_label as y_label_cls
from .active import active as active_cls
from .plot_instantaneous_values import plot_instantaneous_values as plot_instantaneous_values_cls
from .axes import axes as axes_cls
from .curves import curves as curves_cls
from .plot_2 import plot as plot_cls
class report_plots_child(Group):
    """
    'child_object_type' of report_plots.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'plot_window', 'frequency', 'flow_frequency', 'frequency_of',
         'report_defs', 'print', 'title', 'x_label', 'y_label', 'active',
         'plot_instantaneous_values', 'axes', 'curves']

    command_names = \
        ['plot']

    _child_classes = dict(
        name=name_cls,
        plot_window=plot_window_cls,
        frequency=frequency_cls,
        flow_frequency=flow_frequency_cls,
        frequency_of=frequency_of_cls,
        report_defs=report_defs_cls,
        print=print_cls,
        title=title_cls,
        x_label=x_label_cls,
        y_label=y_label_cls,
        active=active_cls,
        plot_instantaneous_values=plot_instantaneous_values_cls,
        axes=axes_cls,
        curves=curves_cls,
        plot=plot_cls,
    )

