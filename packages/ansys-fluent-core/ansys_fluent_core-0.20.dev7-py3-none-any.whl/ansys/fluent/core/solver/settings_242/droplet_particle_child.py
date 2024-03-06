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

from .name import name as name_cls
from .chemical_formula import chemical_formula as chemical_formula_cls
from .density_3 import density as density_cls
from .thermal_conductivity_4 import thermal_conductivity as thermal_conductivity_cls
from .vaporization_model import vaporization_model as vaporization_model_cls
from .thermolysis_model import thermolysis_model as thermolysis_model_cls
from .latent_heat_1 import latent_heat as latent_heat_cls
from .volatile_fraction import volatile_fraction as volatile_fraction_cls
from .heat_of_pyrolysis import heat_of_pyrolysis as heat_of_pyrolysis_cls
from .specific_heat_3 import specific_heat as specific_heat_cls
from .binary_diffusivity_1 import binary_diffusivity as binary_diffusivity_cls
from .diffusivity_reference_pressure import diffusivity_reference_pressure as diffusivity_reference_pressure_cls
from .averaging_coefficient_t import averaging_coefficient_t as averaging_coefficient_t_cls
from .averaging_coefficient_y import averaging_coefficient_y as averaging_coefficient_y_cls
from .vapor_pressure import vapor_pressure as vapor_pressure_cls
from .molecular_weight_1 import molecular_weight as molecular_weight_cls
from .vaporization_temperature import vaporization_temperature as vaporization_temperature_cls
from .boiling_point import boiling_point as boiling_point_cls
from .thermophoretic_co import thermophoretic_co as thermophoretic_co_cls
from .scattering_factor_1 import scattering_factor as scattering_factor_cls
from .emissivity_1 import emissivity as emissivity_cls
from .viscosity_2 import viscosity as viscosity_cls
from .dpm_surften_1 import dpm_surften as dpm_surften_cls
from .electric_conductivity_1 import electric_conductivity as electric_conductivity_cls
from .dual_electric_conductivity_1 import dual_electric_conductivity as dual_electric_conductivity_cls
from .magnetic_permeability import magnetic_permeability as magnetic_permeability_cls
from .charge_density import charge_density as charge_density_cls
from .formation_entropy import formation_entropy as formation_entropy_cls
from .formation_enthalpy import formation_enthalpy as formation_enthalpy_cls
from .reference_temperature_1 import reference_temperature as reference_temperature_cls
class droplet_particle_child(Group):
    """
    'child_object_type' of droplet_particle.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'chemical_formula', 'density', 'thermal_conductivity',
         'vaporization_model', 'thermolysis_model', 'latent_heat',
         'volatile_fraction', 'heat_of_pyrolysis', 'specific_heat',
         'binary_diffusivity', 'diffusivity_reference_pressure',
         'averaging_coefficient_t', 'averaging_coefficient_y',
         'vapor_pressure', 'molecular_weight', 'vaporization_temperature',
         'boiling_point', 'thermophoretic_co', 'scattering_factor',
         'emissivity', 'viscosity', 'dpm_surften', 'electric_conductivity',
         'dual_electric_conductivity', 'magnetic_permeability',
         'charge_density', 'formation_entropy', 'formation_enthalpy',
         'reference_temperature']

    _child_classes = dict(
        name=name_cls,
        chemical_formula=chemical_formula_cls,
        density=density_cls,
        thermal_conductivity=thermal_conductivity_cls,
        vaporization_model=vaporization_model_cls,
        thermolysis_model=thermolysis_model_cls,
        latent_heat=latent_heat_cls,
        volatile_fraction=volatile_fraction_cls,
        heat_of_pyrolysis=heat_of_pyrolysis_cls,
        specific_heat=specific_heat_cls,
        binary_diffusivity=binary_diffusivity_cls,
        diffusivity_reference_pressure=diffusivity_reference_pressure_cls,
        averaging_coefficient_t=averaging_coefficient_t_cls,
        averaging_coefficient_y=averaging_coefficient_y_cls,
        vapor_pressure=vapor_pressure_cls,
        molecular_weight=molecular_weight_cls,
        vaporization_temperature=vaporization_temperature_cls,
        boiling_point=boiling_point_cls,
        thermophoretic_co=thermophoretic_co_cls,
        scattering_factor=scattering_factor_cls,
        emissivity=emissivity_cls,
        viscosity=viscosity_cls,
        dpm_surften=dpm_surften_cls,
        electric_conductivity=electric_conductivity_cls,
        dual_electric_conductivity=dual_electric_conductivity_cls,
        magnetic_permeability=magnetic_permeability_cls,
        charge_density=charge_density_cls,
        formation_entropy=formation_entropy_cls,
        formation_enthalpy=formation_enthalpy_cls,
        reference_temperature=reference_temperature_cls,
    )

