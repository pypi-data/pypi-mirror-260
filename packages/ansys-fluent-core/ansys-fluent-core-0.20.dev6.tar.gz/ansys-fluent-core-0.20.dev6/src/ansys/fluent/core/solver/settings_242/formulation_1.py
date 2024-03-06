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

from .coupled_solver import coupled_solver as coupled_solver_cls
from .segregated_solver import segregated_solver as segregated_solver_cls
from .density_based_solver import density_based_solver as density_based_solver_cls
class formulation(Group):
    """
    Select the pseudo time step size formulation for the pseudo time method.
    """

    fluent_name = "formulation"

    child_names = \
        ['coupled_solver', 'segregated_solver', 'density_based_solver']

    _child_classes = dict(
        coupled_solver=coupled_solver_cls,
        segregated_solver=segregated_solver_cls,
        density_based_solver=density_based_solver_cls,
    )

