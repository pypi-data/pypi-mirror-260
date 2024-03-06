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

from .pressure_gradient_force import pressure_gradient_force as pressure_gradient_force_cls
from .virtual_mass_force import virtual_mass_force as virtual_mass_force_cls
from .volume_displacement_1 import volume_displacement as volume_displacement_cls
from .wall_film import wall_film as wall_film_cls
class physical_models(Group):
    """
    Main menu to enable the required physical submodels for the discrete phase model.
    """

    fluent_name = "physical-models"

    child_names = \
        ['pressure_gradient_force', 'virtual_mass_force',
         'volume_displacement', 'wall_film']

    _child_classes = dict(
        pressure_gradient_force=pressure_gradient_force_cls,
        virtual_mass_force=virtual_mass_force_cls,
        volume_displacement=volume_displacement_cls,
        wall_film=wall_film_cls,
    )

