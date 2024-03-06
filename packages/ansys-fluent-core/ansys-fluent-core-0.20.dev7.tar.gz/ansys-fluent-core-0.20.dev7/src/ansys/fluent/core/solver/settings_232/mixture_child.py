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

from .name_2 import name as name_cls
from .chemical_formula import chemical_formula as chemical_formula_cls
from .density_2 import density as density_cls
from .viscosity_1 import viscosity as viscosity_cls
from .specific_heat_2 import specific_heat as specific_heat_cls
from .thermal_conductivity_2 import thermal_conductivity as thermal_conductivity_cls
from .premix_laminar_speed import premix_laminar_speed as premix_laminar_speed_cls
from .premix_laminar_thickness import premix_laminar_thickness as premix_laminar_thickness_cls
from .premix_unburnt_temp_1 import premix_unburnt_temp as premix_unburnt_temp_cls
from .premix_unburnt_cp import premix_unburnt_cp as premix_unburnt_cp_cls
from .premix_unburnt_density_1 import premix_unburnt_density as premix_unburnt_density_cls
from .premix_heat_trans_coeff_1 import premix_heat_trans_coeff as premix_heat_trans_coeff_cls
from .premix_critical_strain import premix_critical_strain as premix_critical_strain_cls
from .therm_exp_coeff import therm_exp_coeff as therm_exp_coeff_cls
from .absorption_coefficient_1 import absorption_coefficient as absorption_coefficient_cls
from .scattering_coefficient import scattering_coefficient as scattering_coefficient_cls
from .scattering_phase_function import scattering_phase_function as scattering_phase_function_cls
from .refractive_index import refractive_index as refractive_index_cls
from .mass_diffusivity import mass_diffusivity as mass_diffusivity_cls
from .species_1 import species as species_cls
from .reactions_1 import reactions as reactions_cls
from .reaction_mechs import reaction_mechs as reaction_mechs_cls
from .uds_diffusivity import uds_diffusivity as uds_diffusivity_cls
from .thermal_diffusivity import thermal_diffusivity as thermal_diffusivity_cls
from .tmelt import tmelt as tmelt_cls
from .melting_heat import melting_heat as melting_heat_cls
from .eutectic_temp import eutectic_temp as eutectic_temp_cls
from .speed_of_sound import speed_of_sound as speed_of_sound_cls
from .critical_temperature import critical_temperature as critical_temperature_cls
from .critical_pressure import critical_pressure as critical_pressure_cls
from .critical_volume import critical_volume as critical_volume_cls
from .acentric_factor import acentric_factor as acentric_factor_cls
from .electric_conductivity import electric_conductivity as electric_conductivity_cls
from .dual_electric_conductivity import dual_electric_conductivity as dual_electric_conductivity_cls
from .lithium_diffusivity import lithium_diffusivity as lithium_diffusivity_cls
from .collision_cross_section import collision_cross_section as collision_cross_section_cls
class mixture_child(Group):
    """
    'child_object_type' of mixture.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'chemical_formula', 'density', 'viscosity', 'specific_heat',
         'thermal_conductivity', 'premix_laminar_speed',
         'premix_laminar_thickness', 'premix_unburnt_temp',
         'premix_unburnt_cp', 'premix_unburnt_density',
         'premix_heat_trans_coeff', 'premix_critical_strain',
         'therm_exp_coeff', 'absorption_coefficient',
         'scattering_coefficient', 'scattering_phase_function',
         'refractive_index', 'mass_diffusivity', 'species', 'reactions',
         'reaction_mechs', 'uds_diffusivity', 'thermal_diffusivity', 'tmelt',
         'melting_heat', 'eutectic_temp', 'speed_of_sound',
         'critical_temperature', 'critical_pressure', 'critical_volume',
         'acentric_factor', 'electric_conductivity',
         'dual_electric_conductivity', 'lithium_diffusivity',
         'collision_cross_section']

    _child_classes = dict(
        name=name_cls,
        chemical_formula=chemical_formula_cls,
        density=density_cls,
        viscosity=viscosity_cls,
        specific_heat=specific_heat_cls,
        thermal_conductivity=thermal_conductivity_cls,
        premix_laminar_speed=premix_laminar_speed_cls,
        premix_laminar_thickness=premix_laminar_thickness_cls,
        premix_unburnt_temp=premix_unburnt_temp_cls,
        premix_unburnt_cp=premix_unburnt_cp_cls,
        premix_unburnt_density=premix_unburnt_density_cls,
        premix_heat_trans_coeff=premix_heat_trans_coeff_cls,
        premix_critical_strain=premix_critical_strain_cls,
        therm_exp_coeff=therm_exp_coeff_cls,
        absorption_coefficient=absorption_coefficient_cls,
        scattering_coefficient=scattering_coefficient_cls,
        scattering_phase_function=scattering_phase_function_cls,
        refractive_index=refractive_index_cls,
        mass_diffusivity=mass_diffusivity_cls,
        species=species_cls,
        reactions=reactions_cls,
        reaction_mechs=reaction_mechs_cls,
        uds_diffusivity=uds_diffusivity_cls,
        thermal_diffusivity=thermal_diffusivity_cls,
        tmelt=tmelt_cls,
        melting_heat=melting_heat_cls,
        eutectic_temp=eutectic_temp_cls,
        speed_of_sound=speed_of_sound_cls,
        critical_temperature=critical_temperature_cls,
        critical_pressure=critical_pressure_cls,
        critical_volume=critical_volume_cls,
        acentric_factor=acentric_factor_cls,
        electric_conductivity=electric_conductivity_cls,
        dual_electric_conductivity=dual_electric_conductivity_cls,
        lithium_diffusivity=lithium_diffusivity_cls,
        collision_cross_section=collision_cross_section_cls,
    )

