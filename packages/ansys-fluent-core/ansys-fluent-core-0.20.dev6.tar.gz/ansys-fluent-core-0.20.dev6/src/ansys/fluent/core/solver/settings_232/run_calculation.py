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

from .pseudo_time_settings import pseudo_time_settings as pseudo_time_settings_cls
from .iter_count_2 import iter_count as iter_count_cls
from .adaptive_time_stepping import adaptive_time_stepping as adaptive_time_stepping_cls
from .cfl_based_adaptive_time_stepping import cfl_based_adaptive_time_stepping as cfl_based_adaptive_time_stepping_cls
from .reporting_interval import reporting_interval as reporting_interval_cls
from .time_step_count_1 import time_step_count as time_step_count_cls
from .transient_controls import transient_controls as transient_controls_cls
from .data_sampling_1 import data_sampling as data_sampling_cls
from .data_sampling_options import data_sampling_options as data_sampling_options_cls
from .residual_verbosity import residual_verbosity as residual_verbosity_cls
from .calculate import calculate as calculate_cls
from .interrupt import interrupt as interrupt_cls
from .dual_time_iterate import dual_time_iterate as dual_time_iterate_cls
from .iterate import iterate as iterate_cls
from .iterating import iterating as iterating_cls
class run_calculation(Group):
    """
    'run_calculation' child.
    """

    fluent_name = "run-calculation"

    child_names = \
        ['pseudo_time_settings', 'iter_count', 'adaptive_time_stepping',
         'cfl_based_adaptive_time_stepping', 'reporting_interval',
         'time_step_count', 'transient_controls', 'data_sampling',
         'data_sampling_options', 'residual_verbosity']

    command_names = \
        ['calculate', 'interrupt', 'dual_time_iterate', 'iterate']

    query_names = \
        ['iterating']

    _child_classes = dict(
        pseudo_time_settings=pseudo_time_settings_cls,
        iter_count=iter_count_cls,
        adaptive_time_stepping=adaptive_time_stepping_cls,
        cfl_based_adaptive_time_stepping=cfl_based_adaptive_time_stepping_cls,
        reporting_interval=reporting_interval_cls,
        time_step_count=time_step_count_cls,
        transient_controls=transient_controls_cls,
        data_sampling=data_sampling_cls,
        data_sampling_options=data_sampling_options_cls,
        residual_verbosity=residual_verbosity_cls,
        calculate=calculate_cls,
        interrupt=interrupt_cls,
        dual_time_iterate=dual_time_iterate_cls,
        iterate=iterate_cls,
        iterating=iterating_cls,
    )

