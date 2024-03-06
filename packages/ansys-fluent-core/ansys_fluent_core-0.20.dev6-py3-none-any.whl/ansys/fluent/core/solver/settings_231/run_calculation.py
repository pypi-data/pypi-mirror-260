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

from .adaptive_time_stepping import adaptive_time_stepping as adaptive_time_stepping_cls
from .cfl_based_adaptive_time_stepping import cfl_based_adaptive_time_stepping as cfl_based_adaptive_time_stepping_cls
from .data_sampling_1 import data_sampling as data_sampling_cls
from .transient_controls import transient_controls as transient_controls_cls
from .pseudo_time_settings import pseudo_time_settings as pseudo_time_settings_cls
from .data_sampling_options import data_sampling_options as data_sampling_options_cls
from .iter_count_2 import iter_count as iter_count_cls
from .reporting_interval import reporting_interval as reporting_interval_cls
from .residual_verbosity import residual_verbosity as residual_verbosity_cls
from .time_step_count_2 import time_step_count as time_step_count_cls
from .dual_time_iterate import dual_time_iterate as dual_time_iterate_cls
from .iterate import iterate as iterate_cls
from .calculate import calculate as calculate_cls
from .interrupt import interrupt as interrupt_cls
from .iterating import iterating as iterating_cls
class run_calculation(Group):
    """
    'run_calculation' child.
    """

    fluent_name = "run-calculation"

    child_names = \
        ['adaptive_time_stepping', 'cfl_based_adaptive_time_stepping',
         'data_sampling', 'transient_controls', 'pseudo_time_settings',
         'data_sampling_options', 'iter_count', 'reporting_interval',
         'residual_verbosity', 'time_step_count']

    command_names = \
        ['dual_time_iterate', 'iterate', 'calculate', 'interrupt']

    query_names = \
        ['iterating']

    _child_classes = dict(
        adaptive_time_stepping=adaptive_time_stepping_cls,
        cfl_based_adaptive_time_stepping=cfl_based_adaptive_time_stepping_cls,
        data_sampling=data_sampling_cls,
        transient_controls=transient_controls_cls,
        pseudo_time_settings=pseudo_time_settings_cls,
        data_sampling_options=data_sampling_options_cls,
        iter_count=iter_count_cls,
        reporting_interval=reporting_interval_cls,
        residual_verbosity=residual_verbosity_cls,
        time_step_count=time_step_count_cls,
        dual_time_iterate=dual_time_iterate_cls,
        iterate=iterate_cls,
        calculate=calculate_cls,
        interrupt=interrupt_cls,
        iterating=iterating_cls,
    )

