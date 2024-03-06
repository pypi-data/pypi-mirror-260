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

from .enabled_19 import enabled as enabled_cls
from .user_defined_timestep import user_defined_timestep as user_defined_timestep_cls
from .desired_cfl import desired_cfl as desired_cfl_cls
from .time_end import time_end as time_end_cls
from .initial_time_step import initial_time_step as initial_time_step_cls
from .max_fixed_time_step import max_fixed_time_step as max_fixed_time_step_cls
from .update_interval_time_step_size import update_interval_time_step_size as update_interval_time_step_size_cls
from .min_time_step import min_time_step as min_time_step_cls
from .max_time_step import max_time_step as max_time_step_cls
from .min_step_change_factor import min_step_change_factor as min_step_change_factor_cls
from .max_step_change_factor import max_step_change_factor as max_step_change_factor_cls
class cfl_based_adaptive_time_stepping(Group):
    """
    Enter CFL-based adaptive time stepping menu.
    """

    fluent_name = "cfl-based-adaptive-time-stepping"

    child_names = \
        ['enabled', 'user_defined_timestep', 'desired_cfl', 'time_end',
         'initial_time_step', 'max_fixed_time_step',
         'update_interval_time_step_size', 'min_time_step', 'max_time_step',
         'min_step_change_factor', 'max_step_change_factor']

    _child_classes = dict(
        enabled=enabled_cls,
        user_defined_timestep=user_defined_timestep_cls,
        desired_cfl=desired_cfl_cls,
        time_end=time_end_cls,
        initial_time_step=initial_time_step_cls,
        max_fixed_time_step=max_fixed_time_step_cls,
        update_interval_time_step_size=update_interval_time_step_size_cls,
        min_time_step=min_time_step_cls,
        max_time_step=max_time_step_cls,
        min_step_change_factor=min_step_change_factor_cls,
        max_step_change_factor=max_step_change_factor_cls,
    )

