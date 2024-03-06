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

from .discrete_phase_bc_type import discrete_phase_bc_type as discrete_phase_bc_type_cls
from .dem_collision_partner import dem_collision_partner as dem_collision_partner_cls
from .reinj_inj import reinj_inj as reinj_inj_cls
from .dpm_bc_norm_coeff import dpm_bc_norm_coeff as dpm_bc_norm_coeff_cls
from .dpm_bc_tang_coeff import dpm_bc_tang_coeff as dpm_bc_tang_coeff_cls
from .dpm_bc_frictn_coeff import dpm_bc_frictn_coeff as dpm_bc_frictn_coeff_cls
from .discrete_phase_bc_function import discrete_phase_bc_function as discrete_phase_bc_function_cls
from .dpm_film_splash_nsamp import dpm_film_splash_nsamp as dpm_film_splash_nsamp_cls
from .dpm_crit_temp_option import dpm_crit_temp_option as dpm_crit_temp_option_cls
from .dpm_critical_temp_factor import dpm_critical_temp_factor as dpm_critical_temp_factor_cls
from .dpm_calibratable_temp import dpm_calibratable_temp as dpm_calibratable_temp_cls
from .dpm_impingement_splashing_model import dpm_impingement_splashing_model as dpm_impingement_splashing_model_cls
from .dpm_upper_deposition_limit_offset import dpm_upper_deposition_limit_offset as dpm_upper_deposition_limit_offset_cls
from .dpm_deposition_delta_t import dpm_deposition_delta_t as dpm_deposition_delta_t_cls
from .dpm_laplace_number_constant import dpm_laplace_number_constant as dpm_laplace_number_constant_cls
from .dpm_partial_evaporation_ratio import dpm_partial_evaporation_ratio as dpm_partial_evaporation_ratio_cls
from .ra_roughness import ra_roughness as ra_roughness_cls
from .rz_roughness import rz_roughness as rz_roughness_cls
from .rq_roughness import rq_roughness as rq_roughness_cls
from .rsm_roughness import rsm_roughness as rsm_roughness_cls
from .enable_generic_erosion_model import enable_generic_erosion_model as enable_generic_erosion_model_cls
from .generic_impact_angle_function import generic_impact_angle_function as generic_impact_angle_function_cls
from .generic_diameter_function import generic_diameter_function as generic_diameter_function_cls
from .generic_velocity_exponent_function import generic_velocity_exponent_function as generic_velocity_exponent_function_cls
from .enable_finnie_erosion_model import enable_finnie_erosion_model as enable_finnie_erosion_model_cls
from .dpm_bc_erosion_finnie_k import dpm_bc_erosion_finnie_k as dpm_bc_erosion_finnie_k_cls
from .dpm_bc_erosion_finnie_vel_exp import dpm_bc_erosion_finnie_vel_exp as dpm_bc_erosion_finnie_vel_exp_cls
from .dpm_bc_erosion_finnie_max_erosion_angle import dpm_bc_erosion_finnie_max_erosion_angle as dpm_bc_erosion_finnie_max_erosion_angle_cls
from .dpm_bc_erosion_mclaury import dpm_bc_erosion_mclaury as dpm_bc_erosion_mclaury_cls
from .dpm_bc_erosion_mclaury_a import dpm_bc_erosion_mclaury_a as dpm_bc_erosion_mclaury_a_cls
from .dpm_bc_erosion_mclaury_vel_exp import dpm_bc_erosion_mclaury_vel_exp as dpm_bc_erosion_mclaury_vel_exp_cls
from .dpm_bc_erosion_mclaury_transition_angle import dpm_bc_erosion_mclaury_transition_angle as dpm_bc_erosion_mclaury_transition_angle_cls
from .dpm_bc_erosion_mclaury_b import dpm_bc_erosion_mclaury_b as dpm_bc_erosion_mclaury_b_cls
from .dpm_bc_erosion_mclaury_c import dpm_bc_erosion_mclaury_c as dpm_bc_erosion_mclaury_c_cls
from .dpm_bc_erosion_mclaury_w import dpm_bc_erosion_mclaury_w as dpm_bc_erosion_mclaury_w_cls
from .dpm_bc_erosion_mclaury_x import dpm_bc_erosion_mclaury_x as dpm_bc_erosion_mclaury_x_cls
from .dpm_bc_erosion_mclaury_y import dpm_bc_erosion_mclaury_y as dpm_bc_erosion_mclaury_y_cls
from .dpm_bc_erosion_oka import dpm_bc_erosion_oka as dpm_bc_erosion_oka_cls
from .dpm_bc_erosion_oka_e90 import dpm_bc_erosion_oka_e90 as dpm_bc_erosion_oka_e90_cls
from .dpm_bc_erosion_oka_hv import dpm_bc_erosion_oka_hv as dpm_bc_erosion_oka_hv_cls
from .dpm_bc_erosion_oka_n1 import dpm_bc_erosion_oka_n1 as dpm_bc_erosion_oka_n1_cls
from .dpm_bc_erosion_oka_n2 import dpm_bc_erosion_oka_n2 as dpm_bc_erosion_oka_n2_cls
from .dpm_bc_erosion_oka_k2 import dpm_bc_erosion_oka_k2 as dpm_bc_erosion_oka_k2_cls
from .dpm_bc_erosion_oka_k3 import dpm_bc_erosion_oka_k3 as dpm_bc_erosion_oka_k3_cls
from .dpm_bc_erosion_oka_dref import dpm_bc_erosion_oka_dref as dpm_bc_erosion_oka_dref_cls
from .dpm_bc_erosion_oka_vref import dpm_bc_erosion_oka_vref as dpm_bc_erosion_oka_vref_cls
from .dpm_bc_erosion_dnv import dpm_bc_erosion_dnv as dpm_bc_erosion_dnv_cls
from .dpm_bc_erosion_dnv_k import dpm_bc_erosion_dnv_k as dpm_bc_erosion_dnv_k_cls
from .dpm_bc_erosion_dnv_n import dpm_bc_erosion_dnv_n as dpm_bc_erosion_dnv_n_cls
from .dpm_bc_erosion_dnv_ductile import dpm_bc_erosion_dnv_ductile as dpm_bc_erosion_dnv_ductile_cls
from .dpm_bc_erosion_shear import dpm_bc_erosion_shear as dpm_bc_erosion_shear_cls
from .dpm_bc_erosion_shear_v import dpm_bc_erosion_shear_v as dpm_bc_erosion_shear_v_cls
from .dpm_bc_erosion_shear_c import dpm_bc_erosion_shear_c as dpm_bc_erosion_shear_c_cls
from .dpm_bc_erosion_shear_packing_limit import dpm_bc_erosion_shear_packing_limit as dpm_bc_erosion_shear_packing_limit_cls
from .dpm_bc_erosion_shielding import dpm_bc_erosion_shielding as dpm_bc_erosion_shielding_cls
from .dpm_wall_heat_exchange import dpm_wall_heat_exchange as dpm_wall_heat_exchange_cls
from .dpm_film_condensation import dpm_film_condensation as dpm_film_condensation_cls
from .dpm_film_bl_model import dpm_film_bl_model as dpm_film_bl_model_cls
from .dpm_particle_stripping import dpm_particle_stripping as dpm_particle_stripping_cls
from .dpm_critical_shear_stress import dpm_critical_shear_stress as dpm_critical_shear_stress_cls
from .dpm_film_separation_model import dpm_film_separation_model as dpm_film_separation_model_cls
from .dpm_critical_we_number import dpm_critical_we_number as dpm_critical_we_number_cls
from .dpm_film_separation_angle import dpm_film_separation_angle as dpm_film_separation_angle_cls
from .dpm_allow_lwf_to_vof import dpm_allow_lwf_to_vof as dpm_allow_lwf_to_vof_cls
from .dpm_allow_vof_to_lwf import dpm_allow_vof_to_lwf as dpm_allow_vof_to_lwf_cls
from .dpm_initialize_lwf import dpm_initialize_lwf as dpm_initialize_lwf_cls
from .dpm_initial_height import dpm_initial_height as dpm_initial_height_cls
from .film_velocity import film_velocity as film_velocity_cls
from .dpm_initial_temperature import dpm_initial_temperature as dpm_initial_temperature_cls
from .dpm_initial_injection import dpm_initial_injection as dpm_initial_injection_cls
from .film_parcel_surface_area_density import film_parcel_surface_area_density as film_parcel_surface_area_density_cls
from .minimum_number_of_parcels_per_face import minimum_number_of_parcels_per_face as minimum_number_of_parcels_per_face_cls
from .in_situ_data_reduction import in_situ_data_reduction as in_situ_data_reduction_cls
from .data_reduction_1 import data_reduction as data_reduction_cls
from .set_as_eulerian_film_wall import set_as_eulerian_film_wall as set_as_eulerian_film_wall_cls
from .film_condition_type import film_condition_type as film_condition_type_cls
from .film_height import film_height as film_height_cls
from .flux_momentum import flux_momentum as flux_momentum_cls
from .relative_initial_film_velocity import relative_initial_film_velocity as relative_initial_film_velocity_cls
from .include_film_momentum_pressure import include_film_momentum_pressure as include_film_momentum_pressure_cls
from .film_temperature import film_temperature as film_temperature_cls
from .film_passive_scalar import film_passive_scalar as film_passive_scalar_cls
from .enable_film_source_terms import enable_film_source_terms as enable_film_source_terms_cls
from .film_mass_source import film_mass_source as film_mass_source_cls
from .momentum_source import momentum_source as momentum_source_cls
from .film_heat_source import film_heat_source as film_heat_source_cls
from .film_passive_scalar_source import film_passive_scalar_source as film_passive_scalar_source_cls
from .enable_film_phase_change import enable_film_phase_change as enable_film_phase_change_cls
from .phase_change_model import phase_change_model as phase_change_model_cls
from .film_condensation_constant import film_condensation_constant as film_condensation_constant_cls
from .film_vaporization_constant import film_vaporization_constant as film_vaporization_constant_cls
from .film_condensation_rate import film_condensation_rate as film_condensation_rate_cls
from .film_vaporization_rate import film_vaporization_rate as film_vaporization_rate_cls
from .enable_flow_momentum_coupling import enable_flow_momentum_coupling as enable_flow_momentum_coupling_cls
from .enable_dpm_wall_splash import enable_dpm_wall_splash as enable_dpm_wall_splash_cls
from .allow_film_boundary_separation import allow_film_boundary_separation as allow_film_boundary_separation_cls
from .impingement_model_1 import impingement_model as impingement_model_cls
from .number_of_splashed_particles import number_of_splashed_particles as number_of_splashed_particles_cls
from .critical_temperature_factor import critical_temperature_factor as critical_temperature_factor_cls
from .wall_roughness_length_ra import wall_roughness_length_ra as wall_roughness_length_ra_cls
from .wall_roughness_length_rz import wall_roughness_length_rz as wall_roughness_length_rz_cls
from .upper_deposition_limit_offset import upper_deposition_limit_offset as upper_deposition_limit_offset_cls
from .deposition_delta_t import deposition_delta_t as deposition_delta_t_cls
from .laplace_number_constant import laplace_number_constant as laplace_number_constant_cls
from .partial_evaporation_ratio import partial_evaporation_ratio as partial_evaporation_ratio_cls
from .enable_film_contact_angle_force import enable_film_contact_angle_force as enable_film_contact_angle_force_cls
from .film_contact_angle_mean import film_contact_angle_mean as film_contact_angle_mean_cls
from .film_contact_angle_rstd import film_contact_angle_rstd as film_contact_angle_rstd_cls
from .film_contact_angle_beta import film_contact_angle_beta as film_contact_angle_beta_cls
from .film_vof_coupling_high import film_vof_coupling_high as film_vof_coupling_high_cls
from .film_vof_trans_high import film_vof_trans_high as film_vof_trans_high_cls
from .film_vof_trans_high_relax import film_vof_trans_high_relax as film_vof_trans_high_relax_cls
from .film_vof_coupling_low import film_vof_coupling_low as film_vof_coupling_low_cls
from .film_vof_trans_low import film_vof_trans_low as film_vof_trans_low_cls
from .film_vof_trans_low_relax import film_vof_trans_low_relax as film_vof_trans_low_relax_cls
from .dpm_do_initialize_lwf_now import dpm_do_initialize_lwf_now as dpm_do_initialize_lwf_now_cls
class dpm(Group):
    """
    Help not available.
    """

    fluent_name = "dpm"

    child_names = \
        ['discrete_phase_bc_type', 'dem_collision_partner', 'reinj_inj',
         'dpm_bc_norm_coeff', 'dpm_bc_tang_coeff', 'dpm_bc_frictn_coeff',
         'discrete_phase_bc_function', 'dpm_film_splash_nsamp',
         'dpm_crit_temp_option', 'dpm_critical_temp_factor',
         'dpm_calibratable_temp', 'dpm_impingement_splashing_model',
         'dpm_upper_deposition_limit_offset', 'dpm_deposition_delta_t',
         'dpm_laplace_number_constant', 'dpm_partial_evaporation_ratio',
         'ra_roughness', 'rz_roughness', 'rq_roughness', 'rsm_roughness',
         'enable_generic_erosion_model', 'generic_impact_angle_function',
         'generic_diameter_function', 'generic_velocity_exponent_function',
         'enable_finnie_erosion_model', 'dpm_bc_erosion_finnie_k',
         'dpm_bc_erosion_finnie_vel_exp',
         'dpm_bc_erosion_finnie_max_erosion_angle', 'dpm_bc_erosion_mclaury',
         'dpm_bc_erosion_mclaury_a', 'dpm_bc_erosion_mclaury_vel_exp',
         'dpm_bc_erosion_mclaury_transition_angle',
         'dpm_bc_erosion_mclaury_b', 'dpm_bc_erosion_mclaury_c',
         'dpm_bc_erosion_mclaury_w', 'dpm_bc_erosion_mclaury_x',
         'dpm_bc_erosion_mclaury_y', 'dpm_bc_erosion_oka',
         'dpm_bc_erosion_oka_e90', 'dpm_bc_erosion_oka_hv',
         'dpm_bc_erosion_oka_n1', 'dpm_bc_erosion_oka_n2',
         'dpm_bc_erosion_oka_k2', 'dpm_bc_erosion_oka_k3',
         'dpm_bc_erosion_oka_dref', 'dpm_bc_erosion_oka_vref',
         'dpm_bc_erosion_dnv', 'dpm_bc_erosion_dnv_k', 'dpm_bc_erosion_dnv_n',
         'dpm_bc_erosion_dnv_ductile', 'dpm_bc_erosion_shear',
         'dpm_bc_erosion_shear_v', 'dpm_bc_erosion_shear_c',
         'dpm_bc_erosion_shear_packing_limit', 'dpm_bc_erosion_shielding',
         'dpm_wall_heat_exchange', 'dpm_film_condensation',
         'dpm_film_bl_model', 'dpm_particle_stripping',
         'dpm_critical_shear_stress', 'dpm_film_separation_model',
         'dpm_critical_we_number', 'dpm_film_separation_angle',
         'dpm_allow_lwf_to_vof', 'dpm_allow_vof_to_lwf', 'dpm_initialize_lwf',
         'dpm_initial_height', 'film_velocity', 'dpm_initial_temperature',
         'dpm_initial_injection', 'film_parcel_surface_area_density',
         'minimum_number_of_parcels_per_face', 'in_situ_data_reduction',
         'data_reduction', 'set_as_eulerian_film_wall', 'film_condition_type',
         'film_height', 'flux_momentum', 'relative_initial_film_velocity',
         'include_film_momentum_pressure', 'film_temperature',
         'film_passive_scalar', 'enable_film_source_terms',
         'film_mass_source', 'momentum_source', 'film_heat_source',
         'film_passive_scalar_source', 'enable_film_phase_change',
         'phase_change_model', 'film_condensation_constant',
         'film_vaporization_constant', 'film_condensation_rate',
         'film_vaporization_rate', 'enable_flow_momentum_coupling',
         'enable_dpm_wall_splash', 'allow_film_boundary_separation',
         'impingement_model', 'number_of_splashed_particles',
         'critical_temperature_factor', 'wall_roughness_length_ra',
         'wall_roughness_length_rz', 'upper_deposition_limit_offset',
         'deposition_delta_t', 'laplace_number_constant',
         'partial_evaporation_ratio', 'enable_film_contact_angle_force',
         'film_contact_angle_mean', 'film_contact_angle_rstd',
         'film_contact_angle_beta', 'film_vof_coupling_high',
         'film_vof_trans_high', 'film_vof_trans_high_relax',
         'film_vof_coupling_low', 'film_vof_trans_low',
         'film_vof_trans_low_relax']

    command_names = \
        ['dpm_do_initialize_lwf_now']

    _child_classes = dict(
        discrete_phase_bc_type=discrete_phase_bc_type_cls,
        dem_collision_partner=dem_collision_partner_cls,
        reinj_inj=reinj_inj_cls,
        dpm_bc_norm_coeff=dpm_bc_norm_coeff_cls,
        dpm_bc_tang_coeff=dpm_bc_tang_coeff_cls,
        dpm_bc_frictn_coeff=dpm_bc_frictn_coeff_cls,
        discrete_phase_bc_function=discrete_phase_bc_function_cls,
        dpm_film_splash_nsamp=dpm_film_splash_nsamp_cls,
        dpm_crit_temp_option=dpm_crit_temp_option_cls,
        dpm_critical_temp_factor=dpm_critical_temp_factor_cls,
        dpm_calibratable_temp=dpm_calibratable_temp_cls,
        dpm_impingement_splashing_model=dpm_impingement_splashing_model_cls,
        dpm_upper_deposition_limit_offset=dpm_upper_deposition_limit_offset_cls,
        dpm_deposition_delta_t=dpm_deposition_delta_t_cls,
        dpm_laplace_number_constant=dpm_laplace_number_constant_cls,
        dpm_partial_evaporation_ratio=dpm_partial_evaporation_ratio_cls,
        ra_roughness=ra_roughness_cls,
        rz_roughness=rz_roughness_cls,
        rq_roughness=rq_roughness_cls,
        rsm_roughness=rsm_roughness_cls,
        enable_generic_erosion_model=enable_generic_erosion_model_cls,
        generic_impact_angle_function=generic_impact_angle_function_cls,
        generic_diameter_function=generic_diameter_function_cls,
        generic_velocity_exponent_function=generic_velocity_exponent_function_cls,
        enable_finnie_erosion_model=enable_finnie_erosion_model_cls,
        dpm_bc_erosion_finnie_k=dpm_bc_erosion_finnie_k_cls,
        dpm_bc_erosion_finnie_vel_exp=dpm_bc_erosion_finnie_vel_exp_cls,
        dpm_bc_erosion_finnie_max_erosion_angle=dpm_bc_erosion_finnie_max_erosion_angle_cls,
        dpm_bc_erosion_mclaury=dpm_bc_erosion_mclaury_cls,
        dpm_bc_erosion_mclaury_a=dpm_bc_erosion_mclaury_a_cls,
        dpm_bc_erosion_mclaury_vel_exp=dpm_bc_erosion_mclaury_vel_exp_cls,
        dpm_bc_erosion_mclaury_transition_angle=dpm_bc_erosion_mclaury_transition_angle_cls,
        dpm_bc_erosion_mclaury_b=dpm_bc_erosion_mclaury_b_cls,
        dpm_bc_erosion_mclaury_c=dpm_bc_erosion_mclaury_c_cls,
        dpm_bc_erosion_mclaury_w=dpm_bc_erosion_mclaury_w_cls,
        dpm_bc_erosion_mclaury_x=dpm_bc_erosion_mclaury_x_cls,
        dpm_bc_erosion_mclaury_y=dpm_bc_erosion_mclaury_y_cls,
        dpm_bc_erosion_oka=dpm_bc_erosion_oka_cls,
        dpm_bc_erosion_oka_e90=dpm_bc_erosion_oka_e90_cls,
        dpm_bc_erosion_oka_hv=dpm_bc_erosion_oka_hv_cls,
        dpm_bc_erosion_oka_n1=dpm_bc_erosion_oka_n1_cls,
        dpm_bc_erosion_oka_n2=dpm_bc_erosion_oka_n2_cls,
        dpm_bc_erosion_oka_k2=dpm_bc_erosion_oka_k2_cls,
        dpm_bc_erosion_oka_k3=dpm_bc_erosion_oka_k3_cls,
        dpm_bc_erosion_oka_dref=dpm_bc_erosion_oka_dref_cls,
        dpm_bc_erosion_oka_vref=dpm_bc_erosion_oka_vref_cls,
        dpm_bc_erosion_dnv=dpm_bc_erosion_dnv_cls,
        dpm_bc_erosion_dnv_k=dpm_bc_erosion_dnv_k_cls,
        dpm_bc_erosion_dnv_n=dpm_bc_erosion_dnv_n_cls,
        dpm_bc_erosion_dnv_ductile=dpm_bc_erosion_dnv_ductile_cls,
        dpm_bc_erosion_shear=dpm_bc_erosion_shear_cls,
        dpm_bc_erosion_shear_v=dpm_bc_erosion_shear_v_cls,
        dpm_bc_erosion_shear_c=dpm_bc_erosion_shear_c_cls,
        dpm_bc_erosion_shear_packing_limit=dpm_bc_erosion_shear_packing_limit_cls,
        dpm_bc_erosion_shielding=dpm_bc_erosion_shielding_cls,
        dpm_wall_heat_exchange=dpm_wall_heat_exchange_cls,
        dpm_film_condensation=dpm_film_condensation_cls,
        dpm_film_bl_model=dpm_film_bl_model_cls,
        dpm_particle_stripping=dpm_particle_stripping_cls,
        dpm_critical_shear_stress=dpm_critical_shear_stress_cls,
        dpm_film_separation_model=dpm_film_separation_model_cls,
        dpm_critical_we_number=dpm_critical_we_number_cls,
        dpm_film_separation_angle=dpm_film_separation_angle_cls,
        dpm_allow_lwf_to_vof=dpm_allow_lwf_to_vof_cls,
        dpm_allow_vof_to_lwf=dpm_allow_vof_to_lwf_cls,
        dpm_initialize_lwf=dpm_initialize_lwf_cls,
        dpm_initial_height=dpm_initial_height_cls,
        film_velocity=film_velocity_cls,
        dpm_initial_temperature=dpm_initial_temperature_cls,
        dpm_initial_injection=dpm_initial_injection_cls,
        film_parcel_surface_area_density=film_parcel_surface_area_density_cls,
        minimum_number_of_parcels_per_face=minimum_number_of_parcels_per_face_cls,
        in_situ_data_reduction=in_situ_data_reduction_cls,
        data_reduction=data_reduction_cls,
        set_as_eulerian_film_wall=set_as_eulerian_film_wall_cls,
        film_condition_type=film_condition_type_cls,
        film_height=film_height_cls,
        flux_momentum=flux_momentum_cls,
        relative_initial_film_velocity=relative_initial_film_velocity_cls,
        include_film_momentum_pressure=include_film_momentum_pressure_cls,
        film_temperature=film_temperature_cls,
        film_passive_scalar=film_passive_scalar_cls,
        enable_film_source_terms=enable_film_source_terms_cls,
        film_mass_source=film_mass_source_cls,
        momentum_source=momentum_source_cls,
        film_heat_source=film_heat_source_cls,
        film_passive_scalar_source=film_passive_scalar_source_cls,
        enable_film_phase_change=enable_film_phase_change_cls,
        phase_change_model=phase_change_model_cls,
        film_condensation_constant=film_condensation_constant_cls,
        film_vaporization_constant=film_vaporization_constant_cls,
        film_condensation_rate=film_condensation_rate_cls,
        film_vaporization_rate=film_vaporization_rate_cls,
        enable_flow_momentum_coupling=enable_flow_momentum_coupling_cls,
        enable_dpm_wall_splash=enable_dpm_wall_splash_cls,
        allow_film_boundary_separation=allow_film_boundary_separation_cls,
        impingement_model=impingement_model_cls,
        number_of_splashed_particles=number_of_splashed_particles_cls,
        critical_temperature_factor=critical_temperature_factor_cls,
        wall_roughness_length_ra=wall_roughness_length_ra_cls,
        wall_roughness_length_rz=wall_roughness_length_rz_cls,
        upper_deposition_limit_offset=upper_deposition_limit_offset_cls,
        deposition_delta_t=deposition_delta_t_cls,
        laplace_number_constant=laplace_number_constant_cls,
        partial_evaporation_ratio=partial_evaporation_ratio_cls,
        enable_film_contact_angle_force=enable_film_contact_angle_force_cls,
        film_contact_angle_mean=film_contact_angle_mean_cls,
        film_contact_angle_rstd=film_contact_angle_rstd_cls,
        film_contact_angle_beta=film_contact_angle_beta_cls,
        film_vof_coupling_high=film_vof_coupling_high_cls,
        film_vof_trans_high=film_vof_trans_high_cls,
        film_vof_trans_high_relax=film_vof_trans_high_relax_cls,
        film_vof_coupling_low=film_vof_coupling_low_cls,
        film_vof_trans_low=film_vof_trans_low_cls,
        film_vof_trans_low_relax=film_vof_trans_low_relax_cls,
        dpm_do_initialize_lwf_now=dpm_do_initialize_lwf_now_cls,
    )

