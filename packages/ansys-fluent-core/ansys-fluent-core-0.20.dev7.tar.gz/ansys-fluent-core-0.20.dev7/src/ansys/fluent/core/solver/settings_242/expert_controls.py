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

from .number_of_recycled_modes import number_of_recycled_modes as number_of_recycled_modes_cls
from .amg_iterations import amg_iterations as amg_iterations_cls
class expert_controls(Group):
    """
    Residual minimization expert controls menu.
    """

    fluent_name = "expert-controls"

    child_names = \
        ['number_of_recycled_modes', 'amg_iterations']

    _child_classes = dict(
        number_of_recycled_modes=number_of_recycled_modes_cls,
        amg_iterations=amg_iterations_cls,
    )

