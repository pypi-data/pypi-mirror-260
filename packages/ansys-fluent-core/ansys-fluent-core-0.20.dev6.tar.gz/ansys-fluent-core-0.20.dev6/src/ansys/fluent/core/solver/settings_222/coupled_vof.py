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

from .buoyancy_force_linearization import buoyancy_force_linearization as buoyancy_force_linearization_cls
from .blended_treatment_for_buoyancy_forces import blended_treatment_for_buoyancy_forces as blended_treatment_for_buoyancy_forces_cls
class coupled_vof(Group):
    """
    'coupled_vof' child.
    """

    fluent_name = "coupled-vof"

    child_names = \
        ['buoyancy_force_linearization',
         'blended_treatment_for_buoyancy_forces']

    _child_classes = dict(
        buoyancy_force_linearization=buoyancy_force_linearization_cls,
        blended_treatment_for_buoyancy_forces=blended_treatment_for_buoyancy_forces_cls,
    )

