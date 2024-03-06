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

from .density_3 import density as density_cls
from .specific_heat_3 import specific_heat as specific_heat_cls
from .thermal_conductivity_3 import thermal_conductivity as thermal_conductivity_cls
from .thermophoretic_co import thermophoretic_co as thermophoretic_co_cls
from .scattering_factor import scattering_factor as scattering_factor_cls
from .emissivity import emissivity as emissivity_cls
from .viscosity_2 import viscosity as viscosity_cls
from .dpm_surften import dpm_surften as dpm_surften_cls
from .electric_conductivity_1 import electric_conductivity as electric_conductivity_cls
from .dual_electric_conductivity_1 import dual_electric_conductivity as dual_electric_conductivity_cls
from .magnetic_permeability import magnetic_permeability as magnetic_permeability_cls
from .charge_density import charge_density as charge_density_cls
class inert_particle_child(Group):
    """
    'child_object_type' of inert_particle.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['density', 'specific_heat', 'thermal_conductivity',
         'thermophoretic_co', 'scattering_factor', 'emissivity', 'viscosity',
         'dpm_surften', 'electric_conductivity', 'dual_electric_conductivity',
         'magnetic_permeability', 'charge_density']

    _child_classes = dict(
        density=density_cls,
        specific_heat=specific_heat_cls,
        thermal_conductivity=thermal_conductivity_cls,
        thermophoretic_co=thermophoretic_co_cls,
        scattering_factor=scattering_factor_cls,
        emissivity=emissivity_cls,
        viscosity=viscosity_cls,
        dpm_surften=dpm_surften_cls,
        electric_conductivity=electric_conductivity_cls,
        dual_electric_conductivity=dual_electric_conductivity_cls,
        magnetic_permeability=magnetic_permeability_cls,
        charge_density=charge_density_cls,
    )

