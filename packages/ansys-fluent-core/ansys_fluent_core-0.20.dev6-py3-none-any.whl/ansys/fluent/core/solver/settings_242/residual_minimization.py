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

from .number_of_modes import number_of_modes as number_of_modes_cls
from .manual_expert_controls import manual_expert_controls as manual_expert_controls_cls
from .expert_controls import expert_controls as expert_controls_cls
from .default_2 import default as default_cls
class residual_minimization(Group):
    """
    Enter the residual minimization controls menu.
    """

    fluent_name = "residual-minimization"

    child_names = \
        ['number_of_modes', 'manual_expert_controls', 'expert_controls']

    command_names = \
        ['default']

    _child_classes = dict(
        number_of_modes=number_of_modes_cls,
        manual_expert_controls=manual_expert_controls_cls,
        expert_controls=expert_controls_cls,
        default=default_cls,
    )

