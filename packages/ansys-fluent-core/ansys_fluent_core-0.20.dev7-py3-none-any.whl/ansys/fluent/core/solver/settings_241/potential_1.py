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

from .potential_boundary_condition import potential_boundary_condition as potential_boundary_condition_cls
from .potential_boundary_value import potential_boundary_value as potential_boundary_value_cls
from .electrolyte_potential_boundary_condition import electrolyte_potential_boundary_condition as electrolyte_potential_boundary_condition_cls
from .current_density_boundary_value import current_density_boundary_value as current_density_boundary_value_cls
class potential(Group):
    """
    Help not available.
    """

    fluent_name = "potential"

    child_names = \
        ['potential_boundary_condition', 'potential_boundary_value',
         'electrolyte_potential_boundary_condition',
         'current_density_boundary_value']

    _child_classes = dict(
        potential_boundary_condition=potential_boundary_condition_cls,
        potential_boundary_value=potential_boundary_value_cls,
        electrolyte_potential_boundary_condition=electrolyte_potential_boundary_condition_cls,
        current_density_boundary_value=current_density_boundary_value_cls,
    )

