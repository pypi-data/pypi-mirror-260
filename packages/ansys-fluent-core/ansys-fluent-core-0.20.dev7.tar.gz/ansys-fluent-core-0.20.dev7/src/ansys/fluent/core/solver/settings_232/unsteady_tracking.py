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
from .particle_creation_every_particle_step_enabled import particle_creation_every_particle_step_enabled as particle_creation_every_particle_step_enabled_cls
from .dpm_time_step import dpm_time_step as dpm_time_step_cls
from .n_time_steps import n_time_steps as n_time_steps_cls
from .clear_particles_from_domain import clear_particles_from_domain as clear_particles_from_domain_cls
class unsteady_tracking(Group):
    """
    'unsteady_tracking' child.
    """

    fluent_name = "unsteady-tracking"

    child_names = \
        ['option', 'particle_creation_every_particle_step_enabled',
         'dpm_time_step', 'n_time_steps']

    command_names = \
        ['clear_particles_from_domain']

    _child_classes = dict(
        option=option_cls,
        particle_creation_every_particle_step_enabled=particle_creation_every_particle_step_enabled_cls,
        dpm_time_step=dpm_time_step_cls,
        n_time_steps=n_time_steps_cls,
        clear_particles_from_domain=clear_particles_from_domain_cls,
    )

