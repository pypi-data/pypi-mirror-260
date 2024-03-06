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

from .relaxation_factor_child import relaxation_factor_child

class phase_based_vof_discretization(NamedObject[relaxation_factor_child], _CreatableNamedObjectMixin[relaxation_factor_child]):
    """
    'phase_based_vof_discretization' child.
    """

    fluent_name = "phase-based-vof-discretization"

    child_object_type: relaxation_factor_child = relaxation_factor_child
    """
    child_object_type of phase_based_vof_discretization.
    """
