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

from .density_5 import density as density_cls
from .specific_heat_4 import specific_heat as specific_heat_cls
from .species import species as species_cls
from .vp_equilib import vp_equilib as vp_equilib_cls
from .thermal_conductivity_3 import thermal_conductivity as thermal_conductivity_cls
from .viscosity_2 import viscosity as viscosity_cls
from .dpm_surften import dpm_surften as dpm_surften_cls
from .emissivity_2 import emissivity as emissivity_cls
from .scattering_factor_2 import scattering_factor as scattering_factor_cls
from .vaporization_model import vaporization_model as vaporization_model_cls
from .averaging_coefficient_t import averaging_coefficient_t as averaging_coefficient_t_cls
from .averaging_coefficient_y import averaging_coefficient_y as averaging_coefficient_y_cls
from .thermophoretic_co import thermophoretic_co as thermophoretic_co_cls
from .reaction_model import reaction_model as reaction_model_cls
from .mixture_species_1 import mixture_species as mixture_species_cls
class particle_mixture_child(Group):
    """
    'child_object_type' of particle_mixture.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['density', 'specific_heat', 'species', 'vp_equilib',
         'thermal_conductivity', 'viscosity', 'dpm_surften', 'emissivity',
         'scattering_factor', 'vaporization_model', 'averaging_coefficient_t',
         'averaging_coefficient_y', 'thermophoretic_co', 'reaction_model',
         'mixture_species']

    _child_classes = dict(
        density=density_cls,
        specific_heat=specific_heat_cls,
        species=species_cls,
        vp_equilib=vp_equilib_cls,
        thermal_conductivity=thermal_conductivity_cls,
        viscosity=viscosity_cls,
        dpm_surften=dpm_surften_cls,
        emissivity=emissivity_cls,
        scattering_factor=scattering_factor_cls,
        vaporization_model=vaporization_model_cls,
        averaging_coefficient_t=averaging_coefficient_t_cls,
        averaging_coefficient_y=averaging_coefficient_y_cls,
        thermophoretic_co=thermophoretic_co_cls,
        reaction_model=reaction_model_cls,
        mixture_species=mixture_species_cls,
    )

