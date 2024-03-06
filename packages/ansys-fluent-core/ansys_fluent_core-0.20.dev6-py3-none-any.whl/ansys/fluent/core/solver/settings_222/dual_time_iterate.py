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

from .number_of_total_periods import number_of_total_periods as number_of_total_periods_cls
from .number_of_time_steps import number_of_time_steps as number_of_time_steps_cls
from .total_number_of_time_steps import total_number_of_time_steps as total_number_of_time_steps_cls
from .total_time import total_time as total_time_cls
from .incremental_time import incremental_time as incremental_time_cls
from .max_iteration_per_step import max_iteration_per_step as max_iteration_per_step_cls
from .postprocess import postprocess as postprocess_cls
from .num_of_post_iter_per_timestep import num_of_post_iter_per_timestep as num_of_post_iter_per_timestep_cls
class dual_time_iterate(Command):
    """
    Perform unsteady iterations.
    
    Parameters
    ----------
        number_of_total_periods : int
            Set number of total periods.
        number_of_time_steps : int
            Set inceremtal number of Time steps.
        total_number_of_time_steps : int
            Set total number of Time steps.
        total_time : real
            Set Total Simulation Time.
        incremental_time : real
            Set Incremental Time.
        max_iteration_per_step : int
            Set Maximum Number of iterations per time step.
        postprocess : bool
            Enable/Disable Postprocess pollutant solution?.
        num_of_post_iter_per_timestep : int
            Set Number of post-processing iterations per time step.
    
    """

    fluent_name = "dual-time-iterate"

    argument_names = \
        ['number_of_total_periods', 'number_of_time_steps',
         'total_number_of_time_steps', 'total_time', 'incremental_time',
         'max_iteration_per_step', 'postprocess',
         'num_of_post_iter_per_timestep']

    _child_classes = dict(
        number_of_total_periods=number_of_total_periods_cls,
        number_of_time_steps=number_of_time_steps_cls,
        total_number_of_time_steps=total_number_of_time_steps_cls,
        total_time=total_time_cls,
        incremental_time=incremental_time_cls,
        max_iteration_per_step=max_iteration_per_step_cls,
        postprocess=postprocess_cls,
        num_of_post_iter_per_timestep=num_of_post_iter_per_timestep_cls,
    )

