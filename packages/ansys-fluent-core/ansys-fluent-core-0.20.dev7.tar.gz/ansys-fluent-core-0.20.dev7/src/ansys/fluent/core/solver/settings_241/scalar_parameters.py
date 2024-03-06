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

from .fixed_cycle_parameters import fixed_cycle_parameters as fixed_cycle_parameters_cls
from .coarsening_parameters import coarsening_parameters as coarsening_parameters_cls
from .smoother_type import smoother_type as smoother_type_cls
class scalar_parameters(Group):
    """
    Enter AMG scalar parameters menu.
    """

    fluent_name = "scalar-parameters"

    child_names = \
        ['fixed_cycle_parameters', 'coarsening_parameters', 'smoother_type']

    _child_classes = dict(
        fixed_cycle_parameters=fixed_cycle_parameters_cls,
        coarsening_parameters=coarsening_parameters_cls,
        smoother_type=smoother_type_cls,
    )

