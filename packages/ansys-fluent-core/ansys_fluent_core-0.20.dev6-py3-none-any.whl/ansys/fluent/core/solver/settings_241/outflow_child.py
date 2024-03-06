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
from .phase_13 import phase as phase_cls
from .geom_disable import geom_disable as geom_disable_cls
from .geom_dir_spec import geom_dir_spec as geom_dir_spec_cls
from .geom_dir_x import geom_dir_x as geom_dir_x_cls
from .geom_dir_y import geom_dir_y as geom_dir_y_cls
from .geom_dir_z import geom_dir_z as geom_dir_z_cls
from .geom_levels import geom_levels as geom_levels_cls
from .geom_bgthread import geom_bgthread as geom_bgthread_cls
from .flowrate_frac import flowrate_frac as flowrate_frac_cls
from .potential_boundary_condition import potential_boundary_condition as potential_boundary_condition_cls
from .potential_boundary_value import potential_boundary_value as potential_boundary_value_cls
from .electrolyte_potential_boundary_condition import electrolyte_potential_boundary_condition as electrolyte_potential_boundary_condition_cls
from .current_density_boundary_value import current_density_boundary_value as current_density_boundary_value_cls
from .x_displacement_type import x_displacement_type as x_displacement_type_cls
from .x_displacement_value import x_displacement_value as x_displacement_value_cls
from .y_displacement_type import y_displacement_type as y_displacement_type_cls
from .y_displacement_value import y_displacement_value as y_displacement_value_cls
from .z_displacement_type import z_displacement_type as z_displacement_type_cls
from .z_displacement_value import z_displacement_value as z_displacement_value_cls
from .uds_bc import uds_bc as uds_bc_cls
from .uds import uds as uds_cls
from .radiation_bc import radiation_bc as radiation_bc_cls
from .theta_width_of_beam import theta_width_of_beam as theta_width_of_beam_cls
from .phi_width_of_beam import phi_width_of_beam as phi_width_of_beam_cls
from .direct_irradiation import direct_irradiation as direct_irradiation_cls
from .diffuse_irradiation import diffuse_irradiation as diffuse_irradiation_cls
from .parallel_collimated_beam import parallel_collimated_beam as parallel_collimated_beam_cls
from .use_beeam_direction_from_solar_load_model_settings import use_beeam_direction_from_solar_load_model_settings as use_beeam_direction_from_solar_load_model_settings_cls
from .use_irradiation_from_solar_soad_model_settings import use_irradiation_from_solar_soad_model_settings as use_irradiation_from_solar_soad_model_settings_cls
from .external_black_body_temperature_method import external_black_body_temperature_method as external_black_body_temperature_method_cls
from .black_body_temperature import black_body_temperature as black_body_temperature_cls
from .internal_emissivity import internal_emissivity as internal_emissivity_cls
from .discrete_phase_bc_type import discrete_phase_bc_type as discrete_phase_bc_type_cls
from .dem_collision_partner import dem_collision_partner as dem_collision_partner_cls
from .reinj_inj import reinj_inj as reinj_inj_cls
from .discrete_phase_bc_function import discrete_phase_bc_function as discrete_phase_bc_function_cls
from .participates_in_solar_ray_tracing import participates_in_solar_ray_tracing as participates_in_solar_ray_tracing_cls
from .solar_transmissivity_factor import solar_transmissivity_factor as solar_transmissivity_factor_cls
from .radiating_s2s_surface import radiating_s2s_surface as radiating_s2s_surface_cls
class outflow_child(Group):
    """
    'child_object_type' of outflow.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'phase', 'geom_disable', 'geom_dir_spec', 'geom_dir_x',
         'geom_dir_y', 'geom_dir_z', 'geom_levels', 'geom_bgthread',
         'flowrate_frac', 'potential_boundary_condition',
         'potential_boundary_value',
         'electrolyte_potential_boundary_condition',
         'current_density_boundary_value', 'x_displacement_type',
         'x_displacement_value', 'y_displacement_type',
         'y_displacement_value', 'z_displacement_type',
         'z_displacement_value', 'uds_bc', 'uds', 'radiation_bc',
         'theta_width_of_beam', 'phi_width_of_beam', 'direct_irradiation',
         'diffuse_irradiation', 'parallel_collimated_beam',
         'use_beeam_direction_from_solar_load_model_settings',
         'use_irradiation_from_solar_soad_model_settings',
         'external_black_body_temperature_method', 'black_body_temperature',
         'internal_emissivity', 'discrete_phase_bc_type',
         'dem_collision_partner', 'reinj_inj', 'discrete_phase_bc_function',
         'participates_in_solar_ray_tracing', 'solar_transmissivity_factor',
         'radiating_s2s_surface']

    _child_classes = dict(
        name=name_cls,
        phase=phase_cls,
        geom_disable=geom_disable_cls,
        geom_dir_spec=geom_dir_spec_cls,
        geom_dir_x=geom_dir_x_cls,
        geom_dir_y=geom_dir_y_cls,
        geom_dir_z=geom_dir_z_cls,
        geom_levels=geom_levels_cls,
        geom_bgthread=geom_bgthread_cls,
        flowrate_frac=flowrate_frac_cls,
        potential_boundary_condition=potential_boundary_condition_cls,
        potential_boundary_value=potential_boundary_value_cls,
        electrolyte_potential_boundary_condition=electrolyte_potential_boundary_condition_cls,
        current_density_boundary_value=current_density_boundary_value_cls,
        x_displacement_type=x_displacement_type_cls,
        x_displacement_value=x_displacement_value_cls,
        y_displacement_type=y_displacement_type_cls,
        y_displacement_value=y_displacement_value_cls,
        z_displacement_type=z_displacement_type_cls,
        z_displacement_value=z_displacement_value_cls,
        uds_bc=uds_bc_cls,
        uds=uds_cls,
        radiation_bc=radiation_bc_cls,
        theta_width_of_beam=theta_width_of_beam_cls,
        phi_width_of_beam=phi_width_of_beam_cls,
        direct_irradiation=direct_irradiation_cls,
        diffuse_irradiation=diffuse_irradiation_cls,
        parallel_collimated_beam=parallel_collimated_beam_cls,
        use_beeam_direction_from_solar_load_model_settings=use_beeam_direction_from_solar_load_model_settings_cls,
        use_irradiation_from_solar_soad_model_settings=use_irradiation_from_solar_soad_model_settings_cls,
        external_black_body_temperature_method=external_black_body_temperature_method_cls,
        black_body_temperature=black_body_temperature_cls,
        internal_emissivity=internal_emissivity_cls,
        discrete_phase_bc_type=discrete_phase_bc_type_cls,
        dem_collision_partner=dem_collision_partner_cls,
        reinj_inj=reinj_inj_cls,
        discrete_phase_bc_function=discrete_phase_bc_function_cls,
        participates_in_solar_ray_tracing=participates_in_solar_ray_tracing_cls,
        solar_transmissivity_factor=solar_transmissivity_factor_cls,
        radiating_s2s_surface=radiating_s2s_surface_cls,
    )

