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

from .option_3 import option as option_cls
from .create_particles_every_dpm_step import create_particles_every_dpm_step as create_particles_every_dpm_step_cls
from .dpm_time_step_size import dpm_time_step_size as dpm_time_step_size_cls
from .number_of_time_steps import number_of_time_steps as number_of_time_steps_cls
from .clear_all_particles import clear_all_particles as clear_all_particles_cls
class unsteady_tracking(Group):
    """
    'unsteady_tracking' child.
    """

    fluent_name = "unsteady-tracking"

    child_names = \
        ['option', 'create_particles_every_dpm_step', 'dpm_time_step_size',
         'number_of_time_steps']

    command_names = \
        ['clear_all_particles']

    _child_classes = dict(
        option=option_cls,
        create_particles_every_dpm_step=create_particles_every_dpm_step_cls,
        dpm_time_step_size=dpm_time_step_size_cls,
        number_of_time_steps=number_of_time_steps_cls,
        clear_all_particles=clear_all_particles_cls,
    )

