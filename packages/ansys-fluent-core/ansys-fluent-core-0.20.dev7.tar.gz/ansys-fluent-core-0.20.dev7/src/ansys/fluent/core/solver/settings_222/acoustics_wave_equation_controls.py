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

from .expert import expert as expert_cls
from .relative_convergence_criterion import relative_convergence_criterion as relative_convergence_criterion_cls
from .max_iterations_per_timestep import max_iterations_per_timestep as max_iterations_per_timestep_cls
class acoustics_wave_equation_controls(Group):
    """
    'acoustics_wave_equation_controls' child.
    """

    fluent_name = "acoustics-wave-equation-controls"

    child_names = \
        ['expert', 'relative_convergence_criterion',
         'max_iterations_per_timestep']

    _child_classes = dict(
        expert=expert_cls,
        relative_convergence_criterion=relative_convergence_criterion_cls,
        max_iterations_per_timestep=max_iterations_per_timestep_cls,
    )

