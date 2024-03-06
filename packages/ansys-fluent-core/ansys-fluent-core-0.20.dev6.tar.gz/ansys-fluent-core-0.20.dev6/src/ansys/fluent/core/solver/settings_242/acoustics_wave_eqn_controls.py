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

from .expert_7 import expert as expert_cls
from .relative_convergence_criterion import relative_convergence_criterion as relative_convergence_criterion_cls
from .max_iter_per_timestep_count import max_iter_per_timestep_count as max_iter_per_timestep_count_cls
class acoustics_wave_eqn_controls(Group):
    """
    Enter menu for acoustics wave equation solver controls.
    """

    fluent_name = "acoustics-wave-eqn-controls"

    child_names = \
        ['expert', 'relative_convergence_criterion',
         'max_iter_per_timestep_count']

    _child_classes = dict(
        expert=expert_cls,
        relative_convergence_criterion=relative_convergence_criterion_cls,
        max_iter_per_timestep_count=max_iter_per_timestep_count_cls,
    )

