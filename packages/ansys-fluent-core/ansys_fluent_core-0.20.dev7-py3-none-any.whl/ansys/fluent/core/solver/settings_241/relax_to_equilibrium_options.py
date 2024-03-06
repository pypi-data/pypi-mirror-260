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

from .turbulent_rate_constant import turbulent_rate_constant as turbulent_rate_constant_cls
from .chemical_rate_constant import chemical_rate_constant as chemical_rate_constant_cls
from .fuel_species import fuel_species as fuel_species_cls
from .equilibrium_rich_flammability import equilibrium_rich_flammability as equilibrium_rich_flammability_cls
from .equilibrium_rich_flammability_options import equilibrium_rich_flammability_options as equilibrium_rich_flammability_options_cls
class relax_to_equilibrium_options(Group):
    """
    'relax_to_equilibrium_options' child.
    """

    fluent_name = "relax-to-equilibrium-options"

    child_names = \
        ['turbulent_rate_constant', 'chemical_rate_constant', 'fuel_species',
         'equilibrium_rich_flammability',
         'equilibrium_rich_flammability_options']

    _child_classes = dict(
        turbulent_rate_constant=turbulent_rate_constant_cls,
        chemical_rate_constant=chemical_rate_constant_cls,
        fuel_species=fuel_species_cls,
        equilibrium_rich_flammability=equilibrium_rich_flammability_cls,
        equilibrium_rich_flammability_options=equilibrium_rich_flammability_options_cls,
    )

