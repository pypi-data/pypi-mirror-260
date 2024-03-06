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

from .variable_lewis_number import variable_lewis_number as variable_lewis_number_cls
from .use_vapor_species_heat_capacity import use_vapor_species_heat_capacity as use_vapor_species_heat_capacity_cls
class convection_diffusion_controlled(Group):
    """
    'convection_diffusion_controlled' child.
    """

    fluent_name = "convection-diffusion-controlled"

    child_names = \
        ['variable_lewis_number', 'use_vapor_species_heat_capacity']

    _child_classes = dict(
        variable_lewis_number=variable_lewis_number_cls,
        use_vapor_species_heat_capacity=use_vapor_species_heat_capacity_cls,
    )

