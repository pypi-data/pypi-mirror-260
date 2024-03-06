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
from .phase_17 import phase as phase_cls
from .geom_disable import geom_disable as geom_disable_cls
from .geom_dir_spec import geom_dir_spec as geom_dir_spec_cls
from .geom_dir_x import geom_dir_x as geom_dir_x_cls
from .geom_dir_y import geom_dir_y as geom_dir_y_cls
from .geom_dir_z import geom_dir_z as geom_dir_z_cls
from .geom_levels import geom_levels as geom_levels_cls
from .geom_bgthread import geom_bgthread as geom_bgthread_cls
from .gauge_pressure import gauge_pressure as gauge_pressure_cls
from .m_1 import m as m_cls
from .t import t as t_cls
from .non_equil_boundary import non_equil_boundary as non_equil_boundary_cls
from .tve import tve as tve_cls
from .coordinate_system import coordinate_system as coordinate_system_cls
from .flow_direction import flow_direction as flow_direction_cls
from .axis_direction_2 import axis_direction as axis_direction_cls
from .axis_origin_2 import axis_origin as axis_origin_cls
from .turbulent_specification import turbulent_specification as turbulent_specification_cls
from .modified_turbulent_viscosity_1 import modified_turbulent_viscosity as modified_turbulent_viscosity_cls
from .laminar_kinetic_energy_1 import laminar_kinetic_energy as laminar_kinetic_energy_cls
from .intermittency_1 import intermittency as intermittency_cls
from .turbulent_kinetic_energy_1 import turbulent_kinetic_energy as turbulent_kinetic_energy_cls
from .turbulent_dissipation_rate_1 import turbulent_dissipation_rate as turbulent_dissipation_rate_cls
from .specific_dissipation_rate_1 import specific_dissipation_rate as specific_dissipation_rate_cls
from .velocity_variance_scale_1 import velocity_variance_scale as velocity_variance_scale_cls
from .turbulent_intensity_1 import turbulent_intensity as turbulent_intensity_cls
from .turbulent_length_scale_1 import turbulent_length_scale as turbulent_length_scale_cls
from .hydraulic_diameter_1 import hydraulic_diameter as hydraulic_diameter_cls
from .turbulent_viscosity_ratio_real_1 import turbulent_viscosity_ratio_real as turbulent_viscosity_ratio_real_cls
from .turbulent_viscosity_ratio_1 import turbulent_viscosity_ratio as turbulent_viscosity_ratio_cls
from .reynolds_stress_specification import reynolds_stress_specification as reynolds_stress_specification_cls
from .uu_reynolds_stresses_1 import uu_reynolds_stresses as uu_reynolds_stresses_cls
from .vv_reynolds_stresses_1 import vv_reynolds_stresses as vv_reynolds_stresses_cls
from .ww_reynolds_stresses_1 import ww_reynolds_stresses as ww_reynolds_stresses_cls
from .uv_reynolds_stresses_1 import uv_reynolds_stresses as uv_reynolds_stresses_cls
from .vw_reynolds_stresses_1 import vw_reynolds_stresses as vw_reynolds_stresses_cls
from .uw_reynolds_stresses_1 import uw_reynolds_stresses as uw_reynolds_stresses_cls
from .subgrid_kinetic_energy_specification import subgrid_kinetic_energy_specification as subgrid_kinetic_energy_specification_cls
from .subgrid_kinetic_energy import subgrid_kinetic_energy as subgrid_kinetic_energy_cls
from .subgrid_turbulent_intensity import subgrid_turbulent_intensity as subgrid_turbulent_intensity_cls
from .radiation_bc import radiation_bc as radiation_bc_cls
from .radial_direction import radial_direction as radial_direction_cls
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
from .mean_mixture_fraction import mean_mixture_fraction as mean_mixture_fraction_cls
from .mixture_fraction_variance import mixture_fraction_variance as mixture_fraction_variance_cls
from .secondary_mean_mixture_fraction import secondary_mean_mixture_fraction as secondary_mean_mixture_fraction_cls
from .secondary_mixture_fraction_variance import secondary_mixture_fraction_variance as secondary_mixture_fraction_variance_cls
from .specify_species_in_mole_fractions import specify_species_in_mole_fractions as specify_species_in_mole_fractions_cls
from .mf import mf as mf_cls
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
from .mixture_fraction_1 import mixture_fraction as mixture_fraction_cls
from .mode_2_probability_1 import mode_2_probability as mode_2_probability_cls
from .mode_3_probability_1 import mode_3_probability as mode_3_probability_cls
from .pollutant_no_mass_fraction_1 import pollutant_no_mass_fraction as pollutant_no_mass_fraction_cls
from .fraction_1 import fraction as fraction_cls
from .pollutant_nh3_mass_fraction_1 import pollutant_nh3_mass_fraction as pollutant_nh3_mass_fraction_cls
from .pollutant_n2o_mass_fraction_1 import pollutant_n2o_mass_fraction as pollutant_n2o_mass_fraction_cls
from .pollut_urea_1 import pollut_urea as pollut_urea_cls
from .pollut_hnco_1 import pollut_hnco as pollut_hnco_cls
from .pollut_nco_1 import pollut_nco as pollut_nco_cls
from .pollut_so2_1 import pollut_so2 as pollut_so2_cls
from .pollut_h2s_1 import pollut_h2s as pollut_h2s_cls
from .pollut_so3_1 import pollut_so3 as pollut_so3_cls
from .pollut_sh_1 import pollut_sh as pollut_sh_cls
from .pollut_so_1 import pollut_so as pollut_so_cls
from .soot_mass_fraction_1 import soot_mass_fraction as soot_mass_fraction_cls
from .nuclei_1 import nuclei as nuclei_cls
from .tar_mass_fraction_1 import tar_mass_fraction as tar_mass_fraction_cls
from .pollut_hg_1 import pollut_hg as pollut_hg_cls
from .pollut_hgcl2_1 import pollut_hgcl2 as pollut_hgcl2_cls
from .pollut_hcl_1 import pollut_hcl as pollut_hcl_cls
from .pollut_hgo_1 import pollut_hgo as pollut_hgo_cls
from .pollut_cl_1 import pollut_cl as pollut_cl_cls
from .pollut_cl2_1 import pollut_cl2 as pollut_cl2_cls
from .pollut_hgcl_1 import pollut_hgcl as pollut_hgcl_cls
from .pollut_hocl_1 import pollut_hocl as pollut_hocl_cls
from .fensapice_flow_bc_subtype import fensapice_flow_bc_subtype as fensapice_flow_bc_subtype_cls
from .fensapice_drop_bccustom import fensapice_drop_bccustom as fensapice_drop_bccustom_cls
from .fensapice_drop_lwc import fensapice_drop_lwc as fensapice_drop_lwc_cls
from .fensapice_drop_dtemp import fensapice_drop_dtemp as fensapice_drop_dtemp_cls
from .fensapice_drop_ddiam import fensapice_drop_ddiam as fensapice_drop_ddiam_cls
from .fensapice_drop_dv import fensapice_drop_dv as fensapice_drop_dv_cls
from .fensapice_drop_dx import fensapice_drop_dx as fensapice_drop_dx_cls
from .fensapice_drop_dy import fensapice_drop_dy as fensapice_drop_dy_cls
from .fensapice_drop_dz import fensapice_drop_dz as fensapice_drop_dz_cls
from .fensapice_dpm_surface_injection import fensapice_dpm_surface_injection as fensapice_dpm_surface_injection_cls
from .fensapice_dpm_inj_nstream import fensapice_dpm_inj_nstream as fensapice_dpm_inj_nstream_cls
from .fensapice_drop_icc import fensapice_drop_icc as fensapice_drop_icc_cls
from .fensapice_drop_ctemp import fensapice_drop_ctemp as fensapice_drop_ctemp_cls
from .fensapice_drop_cmelt import fensapice_drop_cmelt as fensapice_drop_cmelt_cls
from .fensapice_drop_cdiam import fensapice_drop_cdiam as fensapice_drop_cdiam_cls
from .fensapice_drop_cv import fensapice_drop_cv as fensapice_drop_cv_cls
from .fensapice_drop_cx import fensapice_drop_cx as fensapice_drop_cx_cls
from .fensapice_drop_cy import fensapice_drop_cy as fensapice_drop_cy_cls
from .fensapice_drop_cz import fensapice_drop_cz as fensapice_drop_cz_cls
from .fensapice_drop_vrh import fensapice_drop_vrh as fensapice_drop_vrh_cls
from .fensapice_drop_vrh_1 import fensapice_drop_vrh_1 as fensapice_drop_vrh_1_cls
from .fensapice_drop_vc import fensapice_drop_vc as fensapice_drop_vc_cls
from .uds_bc import uds_bc as uds_bc_cls
from .uds import uds as uds_cls
from .discrete_phase_bc_type import discrete_phase_bc_type as discrete_phase_bc_type_cls
from .dem_collision_partner import dem_collision_partner as dem_collision_partner_cls
from .reinj_inj import reinj_inj as reinj_inj_cls
from .discrete_phase_bc_function import discrete_phase_bc_function as discrete_phase_bc_function_cls
from .participates_in_solar_ray_tracing import participates_in_solar_ray_tracing as participates_in_solar_ray_tracing_cls
from .solar_transmissivity_factor import solar_transmissivity_factor as solar_transmissivity_factor_cls
from .radiating_s2s_surface import radiating_s2s_surface as radiating_s2s_surface_cls
class pressure_far_field_child(Group):
    """
    'child_object_type' of pressure_far_field.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'phase', 'geom_disable', 'geom_dir_spec', 'geom_dir_x',
         'geom_dir_y', 'geom_dir_z', 'geom_levels', 'geom_bgthread',
         'gauge_pressure', 'm', 't', 'non_equil_boundary', 'tve',
         'coordinate_system', 'flow_direction', 'axis_direction',
         'axis_origin', 'turbulent_specification',
         'modified_turbulent_viscosity', 'laminar_kinetic_energy',
         'intermittency', 'turbulent_kinetic_energy',
         'turbulent_dissipation_rate', 'specific_dissipation_rate',
         'velocity_variance_scale', 'turbulent_intensity',
         'turbulent_length_scale', 'hydraulic_diameter',
         'turbulent_viscosity_ratio_real', 'turbulent_viscosity_ratio',
         'reynolds_stress_specification', 'uu_reynolds_stresses',
         'vv_reynolds_stresses', 'ww_reynolds_stresses',
         'uv_reynolds_stresses', 'vw_reynolds_stresses',
         'uw_reynolds_stresses', 'subgrid_kinetic_energy_specification',
         'subgrid_kinetic_energy', 'subgrid_turbulent_intensity',
         'radiation_bc', 'radial_direction', 'theta_width_of_beam',
         'phi_width_of_beam', 'direct_irradiation', 'diffuse_irradiation',
         'parallel_collimated_beam',
         'use_beeam_direction_from_solar_load_model_settings',
         'use_irradiation_from_solar_soad_model_settings',
         'external_black_body_temperature_method', 'black_body_temperature',
         'internal_emissivity', 'mean_mixture_fraction',
         'mixture_fraction_variance', 'secondary_mean_mixture_fraction',
         'secondary_mixture_fraction_variance',
         'specify_species_in_mole_fractions', 'mf',
         'potential_boundary_condition', 'potential_boundary_value',
         'electrolyte_potential_boundary_condition',
         'current_density_boundary_value', 'x_displacement_type',
         'x_displacement_value', 'y_displacement_type',
         'y_displacement_value', 'z_displacement_type',
         'z_displacement_value', 'mixture_fraction', 'mode_2_probability',
         'mode_3_probability', 'pollutant_no_mass_fraction', 'fraction',
         'pollutant_nh3_mass_fraction', 'pollutant_n2o_mass_fraction',
         'pollut_urea', 'pollut_hnco', 'pollut_nco', 'pollut_so2',
         'pollut_h2s', 'pollut_so3', 'pollut_sh', 'pollut_so',
         'soot_mass_fraction', 'nuclei', 'tar_mass_fraction', 'pollut_hg',
         'pollut_hgcl2', 'pollut_hcl', 'pollut_hgo', 'pollut_cl',
         'pollut_cl2', 'pollut_hgcl', 'pollut_hocl',
         'fensapice_flow_bc_subtype', 'fensapice_drop_bccustom',
         'fensapice_drop_lwc', 'fensapice_drop_dtemp', 'fensapice_drop_ddiam',
         'fensapice_drop_dv', 'fensapice_drop_dx', 'fensapice_drop_dy',
         'fensapice_drop_dz', 'fensapice_dpm_surface_injection',
         'fensapice_dpm_inj_nstream', 'fensapice_drop_icc',
         'fensapice_drop_ctemp', 'fensapice_drop_cmelt',
         'fensapice_drop_cdiam', 'fensapice_drop_cv', 'fensapice_drop_cx',
         'fensapice_drop_cy', 'fensapice_drop_cz', 'fensapice_drop_vrh',
         'fensapice_drop_vrh_1', 'fensapice_drop_vc', 'uds_bc', 'uds',
         'discrete_phase_bc_type', 'dem_collision_partner', 'reinj_inj',
         'discrete_phase_bc_function', 'participates_in_solar_ray_tracing',
         'solar_transmissivity_factor', 'radiating_s2s_surface']

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
        gauge_pressure=gauge_pressure_cls,
        m=m_cls,
        t=t_cls,
        non_equil_boundary=non_equil_boundary_cls,
        tve=tve_cls,
        coordinate_system=coordinate_system_cls,
        flow_direction=flow_direction_cls,
        axis_direction=axis_direction_cls,
        axis_origin=axis_origin_cls,
        turbulent_specification=turbulent_specification_cls,
        modified_turbulent_viscosity=modified_turbulent_viscosity_cls,
        laminar_kinetic_energy=laminar_kinetic_energy_cls,
        intermittency=intermittency_cls,
        turbulent_kinetic_energy=turbulent_kinetic_energy_cls,
        turbulent_dissipation_rate=turbulent_dissipation_rate_cls,
        specific_dissipation_rate=specific_dissipation_rate_cls,
        velocity_variance_scale=velocity_variance_scale_cls,
        turbulent_intensity=turbulent_intensity_cls,
        turbulent_length_scale=turbulent_length_scale_cls,
        hydraulic_diameter=hydraulic_diameter_cls,
        turbulent_viscosity_ratio_real=turbulent_viscosity_ratio_real_cls,
        turbulent_viscosity_ratio=turbulent_viscosity_ratio_cls,
        reynolds_stress_specification=reynolds_stress_specification_cls,
        uu_reynolds_stresses=uu_reynolds_stresses_cls,
        vv_reynolds_stresses=vv_reynolds_stresses_cls,
        ww_reynolds_stresses=ww_reynolds_stresses_cls,
        uv_reynolds_stresses=uv_reynolds_stresses_cls,
        vw_reynolds_stresses=vw_reynolds_stresses_cls,
        uw_reynolds_stresses=uw_reynolds_stresses_cls,
        subgrid_kinetic_energy_specification=subgrid_kinetic_energy_specification_cls,
        subgrid_kinetic_energy=subgrid_kinetic_energy_cls,
        subgrid_turbulent_intensity=subgrid_turbulent_intensity_cls,
        radiation_bc=radiation_bc_cls,
        radial_direction=radial_direction_cls,
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
        mean_mixture_fraction=mean_mixture_fraction_cls,
        mixture_fraction_variance=mixture_fraction_variance_cls,
        secondary_mean_mixture_fraction=secondary_mean_mixture_fraction_cls,
        secondary_mixture_fraction_variance=secondary_mixture_fraction_variance_cls,
        specify_species_in_mole_fractions=specify_species_in_mole_fractions_cls,
        mf=mf_cls,
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
        mixture_fraction=mixture_fraction_cls,
        mode_2_probability=mode_2_probability_cls,
        mode_3_probability=mode_3_probability_cls,
        pollutant_no_mass_fraction=pollutant_no_mass_fraction_cls,
        fraction=fraction_cls,
        pollutant_nh3_mass_fraction=pollutant_nh3_mass_fraction_cls,
        pollutant_n2o_mass_fraction=pollutant_n2o_mass_fraction_cls,
        pollut_urea=pollut_urea_cls,
        pollut_hnco=pollut_hnco_cls,
        pollut_nco=pollut_nco_cls,
        pollut_so2=pollut_so2_cls,
        pollut_h2s=pollut_h2s_cls,
        pollut_so3=pollut_so3_cls,
        pollut_sh=pollut_sh_cls,
        pollut_so=pollut_so_cls,
        soot_mass_fraction=soot_mass_fraction_cls,
        nuclei=nuclei_cls,
        tar_mass_fraction=tar_mass_fraction_cls,
        pollut_hg=pollut_hg_cls,
        pollut_hgcl2=pollut_hgcl2_cls,
        pollut_hcl=pollut_hcl_cls,
        pollut_hgo=pollut_hgo_cls,
        pollut_cl=pollut_cl_cls,
        pollut_cl2=pollut_cl2_cls,
        pollut_hgcl=pollut_hgcl_cls,
        pollut_hocl=pollut_hocl_cls,
        fensapice_flow_bc_subtype=fensapice_flow_bc_subtype_cls,
        fensapice_drop_bccustom=fensapice_drop_bccustom_cls,
        fensapice_drop_lwc=fensapice_drop_lwc_cls,
        fensapice_drop_dtemp=fensapice_drop_dtemp_cls,
        fensapice_drop_ddiam=fensapice_drop_ddiam_cls,
        fensapice_drop_dv=fensapice_drop_dv_cls,
        fensapice_drop_dx=fensapice_drop_dx_cls,
        fensapice_drop_dy=fensapice_drop_dy_cls,
        fensapice_drop_dz=fensapice_drop_dz_cls,
        fensapice_dpm_surface_injection=fensapice_dpm_surface_injection_cls,
        fensapice_dpm_inj_nstream=fensapice_dpm_inj_nstream_cls,
        fensapice_drop_icc=fensapice_drop_icc_cls,
        fensapice_drop_ctemp=fensapice_drop_ctemp_cls,
        fensapice_drop_cmelt=fensapice_drop_cmelt_cls,
        fensapice_drop_cdiam=fensapice_drop_cdiam_cls,
        fensapice_drop_cv=fensapice_drop_cv_cls,
        fensapice_drop_cx=fensapice_drop_cx_cls,
        fensapice_drop_cy=fensapice_drop_cy_cls,
        fensapice_drop_cz=fensapice_drop_cz_cls,
        fensapice_drop_vrh=fensapice_drop_vrh_cls,
        fensapice_drop_vrh_1=fensapice_drop_vrh_1_cls,
        fensapice_drop_vc=fensapice_drop_vc_cls,
        uds_bc=uds_bc_cls,
        uds=uds_cls,
        discrete_phase_bc_type=discrete_phase_bc_type_cls,
        dem_collision_partner=dem_collision_partner_cls,
        reinj_inj=reinj_inj_cls,
        discrete_phase_bc_function=discrete_phase_bc_function_cls,
        participates_in_solar_ray_tracing=participates_in_solar_ray_tracing_cls,
        solar_transmissivity_factor=solar_transmissivity_factor_cls,
        radiating_s2s_surface=radiating_s2s_surface_cls,
    )

