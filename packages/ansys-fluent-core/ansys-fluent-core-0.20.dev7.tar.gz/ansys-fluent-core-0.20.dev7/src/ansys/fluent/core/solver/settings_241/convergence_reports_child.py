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
from .previous_values_to_consider import previous_values_to_consider as previous_values_to_consider_cls
from .initial_values_to_ignore import initial_values_to_ignore as initial_values_to_ignore_cls
from .iteration_at_creation_or_edit import iteration_at_creation_or_edit as iteration_at_creation_or_edit_cls
from .stop_criterion import stop_criterion as stop_criterion_cls
from .report_defs_1 import report_defs as report_defs_cls
from .print_3 import print as print_cls
from .plot_3 import plot as plot_cls
from .cov import cov as cov_cls
from .active import active as active_cls
from .x_label import x_label as x_label_cls
from .previous_values import previous_values as previous_values_cls
class convergence_reports_child(Group):
    """
    'child_object_type' of convergence_reports.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'previous_values_to_consider', 'initial_values_to_ignore',
         'iteration_at_creation_or_edit', 'stop_criterion', 'report_defs',
         'print', 'plot', 'cov', 'active', 'x_label', 'previous_values']

    _child_classes = dict(
        name=name_cls,
        previous_values_to_consider=previous_values_to_consider_cls,
        initial_values_to_ignore=initial_values_to_ignore_cls,
        iteration_at_creation_or_edit=iteration_at_creation_or_edit_cls,
        stop_criterion=stop_criterion_cls,
        report_defs=report_defs_cls,
        print=print_cls,
        plot=plot_cls,
        cov=cov_cls,
        active=active_cls,
        x_label=x_label_cls,
        previous_values=previous_values_cls,
    )

