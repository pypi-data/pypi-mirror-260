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

from .geom_disable import geom_disable as geom_disable_cls
from .geom_dir_spec import geom_dir_spec as geom_dir_spec_cls
from .geom_dir_x import geom_dir_x as geom_dir_x_cls
from .geom_dir_y import geom_dir_y as geom_dir_y_cls
from .geom_dir_z import geom_dir_z as geom_dir_z_cls
from .geom_levels import geom_levels as geom_levels_cls
from .geom_bgthread import geom_bgthread as geom_bgthread_cls
from .d import d as d_cls
from .q_dot import q_dot as q_dot_cls
from .material_1 import material as material_cls
from .thermal_bc import thermal_bc as thermal_bc_cls
from .t import t as t_cls
from .q import q as q_cls
from .h import h as h_cls
from .tinf_1 import tinf as tinf_cls
from .planar_conduction import planar_conduction as planar_conduction_cls
from .shell_conduction import shell_conduction as shell_conduction_cls
from .thin_wall import thin_wall as thin_wall_cls
from .motion_bc import motion_bc as motion_bc_cls
from .shear_bc import shear_bc as shear_bc_cls
from .rough_bc import rough_bc as rough_bc_cls
from .moving import moving as moving_cls
from .relative import relative as relative_cls
from .rotating import rotating as rotating_cls
from .vmag import vmag as vmag_cls
from .wall_translation import wall_translation as wall_translation_cls
from .components_1 import components as components_cls
from .velocity_1 import velocity as velocity_cls
from .in_emiss import in_emiss as in_emiss_cls
from .ex_emiss import ex_emiss as ex_emiss_cls
from .trad import trad as trad_cls
from .int_rad import int_rad as int_rad_cls
from .trad_internal import trad_internal as trad_internal_cls
from .area_enhancement_factor import area_enhancement_factor as area_enhancement_factor_cls
from .rough_option import rough_option as rough_option_cls
from .rough_nasa import rough_nasa as rough_nasa_cls
from .rough_shin_et_al import rough_shin_et_al as rough_shin_et_al_cls
from .rough_data import rough_data as rough_data_cls
from .roughness_height import roughness_height as roughness_height_cls
from .roughness_const import roughness_const as roughness_const_cls
from .roughness_height_cp import roughness_height_cp as roughness_height_cp_cls
from .roughness_const_cp import roughness_const_cp as roughness_const_cp_cls
from .roughness_const_nasa import roughness_const_nasa as roughness_const_nasa_cls
from .roughness_const_shin import roughness_const_shin as roughness_const_shin_cls
from .roughness_const_data import roughness_const_data as roughness_const_data_cls
from .variable_roughness import variable_roughness as variable_roughness_cls
from .free_stream_velocity import free_stream_velocity as free_stream_velocity_cls
from .free_stream_temp import free_stream_temp as free_stream_temp_cls
from .characteristic_length import characteristic_length as characteristic_length_cls
from .free_stream_temp_cp import free_stream_temp_cp as free_stream_temp_cp_cls
from .characteristic_length_cp import characteristic_length_cp as characteristic_length_cp_cls
from .liquid_content import liquid_content as liquid_content_cls
from .liquid_content_cp import liquid_content_cp as liquid_content_cp_cls
from .droplet_diameter import droplet_diameter as droplet_diameter_cls
from .dpm_bc_type import dpm_bc_type as dpm_bc_type_cls
from .dpm_bc_collision_partner import dpm_bc_collision_partner as dpm_bc_collision_partner_cls
from .reinj_inj import reinj_inj as reinj_inj_cls
from .dpm_bc_norm_coeff import dpm_bc_norm_coeff as dpm_bc_norm_coeff_cls
from .dpm_bc_tang_coeff import dpm_bc_tang_coeff as dpm_bc_tang_coeff_cls
from .dpm_bc_frictn_coeff import dpm_bc_frictn_coeff as dpm_bc_frictn_coeff_cls
from .dpm_bc_udf import dpm_bc_udf as dpm_bc_udf_cls
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
from .dpm_bc_erosion_generic import dpm_bc_erosion_generic as dpm_bc_erosion_generic_cls
from .dpm_bc_erosion import dpm_bc_erosion as dpm_bc_erosion_cls
from .dpm_bc_erosion_c import dpm_bc_erosion_c as dpm_bc_erosion_c_cls
from .dpm_bc_erosion_n import dpm_bc_erosion_n as dpm_bc_erosion_n_cls
from .dpm_bc_erosion_finnie import dpm_bc_erosion_finnie as dpm_bc_erosion_finnie_cls
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
from .band_in_emiss import band_in_emiss as band_in_emiss_cls
from .radiation_bc import radiation_bc as radiation_bc_cls
from .mc_bsource_p import mc_bsource_p as mc_bsource_p_cls
from .mc_poldfun_p import mc_poldfun_p as mc_poldfun_p_cls
from .polar_func_type import polar_func_type as polar_func_type_cls
from .mc_polar_expr import mc_polar_expr as mc_polar_expr_cls
from .polar_pair_list import polar_pair_list as polar_pair_list_cls
from .pold_pair_list_rad import pold_pair_list_rad as pold_pair_list_rad_cls
from .radiation_direction import radiation_direction as radiation_direction_cls
from .coll_dtheta import coll_dtheta as coll_dtheta_cls
from .coll_dphi import coll_dphi as coll_dphi_cls
from .band_q_irrad import band_q_irrad as band_q_irrad_cls
from .band_q_irrad_diffuse import band_q_irrad_diffuse as band_q_irrad_diffuse_cls
from .band_diffuse_frac import band_diffuse_frac as band_diffuse_frac_cls
from .radiating_s2s_surface import radiating_s2s_surface as radiating_s2s_surface_cls
from .critical_zone import critical_zone as critical_zone_cls
from .fpsc import fpsc as fpsc_cls
from .parallel_collimated_beam import parallel_collimated_beam as parallel_collimated_beam_cls
from .solar_fluxes import solar_fluxes as solar_fluxes_cls
from .solar_direction import solar_direction as solar_direction_cls
from .solar_irradiation import solar_irradiation as solar_irradiation_cls
from .v_transmissivity import v_transmissivity as v_transmissivity_cls
from .ir_transmissivity import ir_transmissivity as ir_transmissivity_cls
from .v_opq_absorbtivity import v_opq_absorbtivity as v_opq_absorbtivity_cls
from .ir_opq_absorbtivity import ir_opq_absorbtivity as ir_opq_absorbtivity_cls
from .v_st_absorbtivity import v_st_absorbtivity as v_st_absorbtivity_cls
from .ir_st_absorbtivity import ir_st_absorbtivity as ir_st_absorbtivity_cls
from .d_st_absorbtivity import d_st_absorbtivity as d_st_absorbtivity_cls
from .d_transmissivity import d_transmissivity as d_transmissivity_cls
from .fsi_interface import fsi_interface as fsi_interface_cls
from .react import react as react_cls
from .partially_catalytic import partially_catalytic as partially_catalytic_cls
from .partially_catalytic_material import partially_catalytic_material as partially_catalytic_material_cls
from .partially_catalytic_recombination_coefficient_o import partially_catalytic_recombination_coefficient_o as partially_catalytic_recombination_coefficient_o_cls
from .partially_catalytic_recombination_coefficient_n import partially_catalytic_recombination_coefficient_n as partially_catalytic_recombination_coefficient_n_cls
from .partially_catalytic_recombination_model import partially_catalytic_recombination_model as partially_catalytic_recombination_model_cls
from .species_spec import species_spec as species_spec_cls
from .mf import mf as mf_cls
from .elec_potential_type import elec_potential_type as elec_potential_type_cls
from .potential_value import potential_value as potential_value_cls
from .elec_potential_jump import elec_potential_jump as elec_potential_jump_cls
from .elec_potential_resistance import elec_potential_resistance as elec_potential_resistance_cls
from .dual_potential_type import dual_potential_type as dual_potential_type_cls
from .dual_potential_value import dual_potential_value as dual_potential_value_cls
from .echem_reaction import echem_reaction as echem_reaction_cls
from .elec_potential_mechs import elec_potential_mechs as elec_potential_mechs_cls
from .faradaic_heat import faradaic_heat as faradaic_heat_cls
from .li_ion_type import li_ion_type as li_ion_type_cls
from .li_ion_value import li_ion_value as li_ion_value_cls
from .x_displacement_type import x_displacement_type as x_displacement_type_cls
from .x_displacement_value import x_displacement_value as x_displacement_value_cls
from .y_displacement_type import y_displacement_type as y_displacement_type_cls
from .y_displacement_value import y_displacement_value as y_displacement_value_cls
from .z_displacement_type import z_displacement_type as z_displacement_type_cls
from .z_displacement_value import z_displacement_value as z_displacement_value_cls
from .per_dispx import per_dispx as per_dispx_cls
from .per_dispy import per_dispy as per_dispy_cls
from .per_dispz import per_dispz as per_dispz_cls
from .per_imagx import per_imagx as per_imagx_cls
from .per_imagy import per_imagy as per_imagy_cls
from .per_imagz import per_imagz as per_imagz_cls
from .freq import freq as freq_cls
from .amp import amp as amp_cls
from .nodal_diam import nodal_diam as nodal_diam_cls
from .pass_number import pass_number as pass_number_cls
from .fwd import fwd as fwd_cls
from .aero import aero as aero_cls
from .cmplx import cmplx as cmplx_cls
from .norm import norm as norm_cls
from .method_2 import method as method_cls
from .uds_bc import uds_bc as uds_bc_cls
from .uds import uds as uds_cls
from .gtemp_bc import gtemp_bc as gtemp_bc_cls
from .g_temperature import g_temperature as g_temperature_cls
from .g_qflux import g_qflux as g_qflux_cls
from .wall_restitution_coeff import wall_restitution_coeff as wall_restitution_coeff_cls
from .omega import omega as omega_cls
from .rotation_axis_origin import rotation_axis_origin as rotation_axis_origin_cls
from .rotation_axis_direction import rotation_axis_direction as rotation_axis_direction_cls
from .adhesion_angle import adhesion_angle as adhesion_angle_cls
from .specified_shear import specified_shear as specified_shear_cls
from .shear_stress import shear_stress as shear_stress_cls
from .fslip import fslip as fslip_cls
from .eslip import eslip as eslip_cls
from .surf_tens_grad import surf_tens_grad as surf_tens_grad_cls
from .contact_resistance import contact_resistance as contact_resistance_cls
from .reaction_mechs_1 import reaction_mechs as reaction_mechs_cls
from .surf_washcoat_factor import surf_washcoat_factor as surf_washcoat_factor_cls
from .initial_deposition_height import initial_deposition_height as initial_deposition_height_cls
from .solid_species_density import solid_species_density as solid_species_density_cls
from .ablation_select_model import ablation_select_model as ablation_select_model_cls
from .ablation_vielle_a import ablation_vielle_a as ablation_vielle_a_cls
from .ablation_vielle_n import ablation_vielle_n as ablation_vielle_n_cls
from .ablation_flux import ablation_flux as ablation_flux_cls
from .ablation_surfacerxn_density import ablation_surfacerxn_density as ablation_surfacerxn_density_cls
from .ablation_species_mf import ablation_species_mf as ablation_species_mf_cls
from .specular_coeff import specular_coeff as specular_coeff_cls
from .mom_accom_coef import mom_accom_coef as mom_accom_coef_cls
from .therm_accom_coef import therm_accom_coef as therm_accom_coef_cls
from .eve_accom_coef import eve_accom_coef as eve_accom_coef_cls
from .film_wall import film_wall as film_wall_cls
from .film_wall_bc import film_wall_bc as film_wall_bc_cls
from .film_height import film_height as film_height_cls
from .flux_momentum import flux_momentum as flux_momentum_cls
from .film_relative_vel import film_relative_vel as film_relative_vel_cls
from .film_bc_imp_press import film_bc_imp_press as film_bc_imp_press_cls
from .film_temperature import film_temperature as film_temperature_cls
from .film_scalar import film_scalar as film_scalar_cls
from .film_source import film_source as film_source_cls
from .film_h_src import film_h_src as film_h_src_cls
from .momentum_source import momentum_source as momentum_source_cls
from .film_t_src import film_t_src as film_t_src_cls
from .film_s_src import film_s_src as film_s_src_cls
from .film_phase_change import film_phase_change as film_phase_change_cls
from .film_phase_change_model import film_phase_change_model as film_phase_change_model_cls
from .film_cond_const import film_cond_const as film_cond_const_cls
from .film_vapo_const import film_vapo_const as film_vapo_const_cls
from .film_cond_rate import film_cond_rate as film_cond_rate_cls
from .film_vapo_rate import film_vapo_rate as film_vapo_rate_cls
from .film_momentum_coupling import film_momentum_coupling as film_momentum_coupling_cls
from .film_splash_wall import film_splash_wall as film_splash_wall_cls
from .film_boundary_separation import film_boundary_separation as film_boundary_separation_cls
from .film_impinge_model import film_impinge_model as film_impinge_model_cls
from .film_splash_nparc import film_splash_nparc as film_splash_nparc_cls
from .film_crit_temp_factor import film_crit_temp_factor as film_crit_temp_factor_cls
from .film_roughness_ra import film_roughness_ra as film_roughness_ra_cls
from .film_roughness_rz import film_roughness_rz as film_roughness_rz_cls
from .film_upper_deposition_limit_offset import film_upper_deposition_limit_offset as film_upper_deposition_limit_offset_cls
from .film_deposition_delta_t import film_deposition_delta_t as film_deposition_delta_t_cls
from .film_laplace_number_constant import film_laplace_number_constant as film_laplace_number_constant_cls
from .film_partial_evap_ratio import film_partial_evap_ratio as film_partial_evap_ratio_cls
from .film_contact_angle import film_contact_angle as film_contact_angle_cls
from .film_contact_angle_mean import film_contact_angle_mean as film_contact_angle_mean_cls
from .film_contact_angle_rstd import film_contact_angle_rstd as film_contact_angle_rstd_cls
from .film_contact_angle_beta import film_contact_angle_beta as film_contact_angle_beta_cls
from .film_vof_coupling_high import film_vof_coupling_high as film_vof_coupling_high_cls
from .film_vof_trans_high import film_vof_trans_high as film_vof_trans_high_cls
from .film_vof_trans_high_relax import film_vof_trans_high_relax as film_vof_trans_high_relax_cls
from .film_vof_coupling_low import film_vof_coupling_low as film_vof_coupling_low_cls
from .film_vof_trans_low import film_vof_trans_low as film_vof_trans_low_cls
from .film_vof_trans_low_relax import film_vof_trans_low_relax as film_vof_trans_low_relax_cls
from .caf import caf as caf_cls
from .thermal_stabilization import thermal_stabilization as thermal_stabilization_cls
from .scale_factor import scale_factor as scale_factor_cls
from .stab_method import stab_method as stab_method_cls
from .fensapice_flow_bc_subtype import fensapice_flow_bc_subtype as fensapice_flow_bc_subtype_cls
from .fensapice_ice_icing_mode import fensapice_ice_icing_mode as fensapice_ice_icing_mode_cls
from .fensapice_ice_hflux import fensapice_ice_hflux as fensapice_ice_hflux_cls
from .fensapice_ice_hflux_1 import fensapice_ice_hflux_1 as fensapice_ice_hflux_1_cls
from .fensapice_drop_vwet import fensapice_drop_vwet as fensapice_drop_vwet_cls
class phase_child(Group):
    """
    'child_object_type' of phase.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['geom_disable', 'geom_dir_spec', 'geom_dir_x', 'geom_dir_y',
         'geom_dir_z', 'geom_levels', 'geom_bgthread', 'd', 'q_dot',
         'material', 'thermal_bc', 't', 'q', 'h', 'tinf', 'planar_conduction',
         'shell_conduction', 'thin_wall', 'motion_bc', 'shear_bc', 'rough_bc',
         'moving', 'relative', 'rotating', 'vmag', 'wall_translation',
         'components', 'velocity', 'in_emiss', 'ex_emiss', 'trad', 'int_rad',
         'trad_internal', 'area_enhancement_factor', 'rough_option',
         'rough_nasa', 'rough_shin_et_al', 'rough_data', 'roughness_height',
         'roughness_const', 'roughness_height_cp', 'roughness_const_cp',
         'roughness_const_nasa', 'roughness_const_shin',
         'roughness_const_data', 'variable_roughness', 'free_stream_velocity',
         'free_stream_temp', 'characteristic_length', 'free_stream_temp_cp',
         'characteristic_length_cp', 'liquid_content', 'liquid_content_cp',
         'droplet_diameter', 'dpm_bc_type', 'dpm_bc_collision_partner',
         'reinj_inj', 'dpm_bc_norm_coeff', 'dpm_bc_tang_coeff',
         'dpm_bc_frictn_coeff', 'dpm_bc_udf', 'dpm_film_splash_nsamp',
         'dpm_crit_temp_option', 'dpm_critical_temp_factor',
         'dpm_calibratable_temp', 'dpm_impingement_splashing_model',
         'dpm_upper_deposition_limit_offset', 'dpm_deposition_delta_t',
         'dpm_laplace_number_constant', 'dpm_partial_evaporation_ratio',
         'ra_roughness', 'rz_roughness', 'rq_roughness', 'rsm_roughness',
         'dpm_bc_erosion_generic', 'dpm_bc_erosion', 'dpm_bc_erosion_c',
         'dpm_bc_erosion_n', 'dpm_bc_erosion_finnie',
         'dpm_bc_erosion_finnie_k', 'dpm_bc_erosion_finnie_vel_exp',
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
         'minimum_number_of_parcels_per_face', 'band_in_emiss',
         'radiation_bc', 'mc_bsource_p', 'mc_poldfun_p', 'polar_func_type',
         'mc_polar_expr', 'polar_pair_list', 'pold_pair_list_rad',
         'radiation_direction', 'coll_dtheta', 'coll_dphi', 'band_q_irrad',
         'band_q_irrad_diffuse', 'band_diffuse_frac', 'radiating_s2s_surface',
         'critical_zone', 'fpsc', 'parallel_collimated_beam', 'solar_fluxes',
         'solar_direction', 'solar_irradiation', 'v_transmissivity',
         'ir_transmissivity', 'v_opq_absorbtivity', 'ir_opq_absorbtivity',
         'v_st_absorbtivity', 'ir_st_absorbtivity', 'd_st_absorbtivity',
         'd_transmissivity', 'fsi_interface', 'react', 'partially_catalytic',
         'partially_catalytic_material',
         'partially_catalytic_recombination_coefficient_o',
         'partially_catalytic_recombination_coefficient_n',
         'partially_catalytic_recombination_model', 'species_spec', 'mf',
         'elec_potential_type', 'potential_value', 'elec_potential_jump',
         'elec_potential_resistance', 'dual_potential_type',
         'dual_potential_value', 'echem_reaction', 'elec_potential_mechs',
         'faradaic_heat', 'li_ion_type', 'li_ion_value',
         'x_displacement_type', 'x_displacement_value', 'y_displacement_type',
         'y_displacement_value', 'z_displacement_type',
         'z_displacement_value', 'per_dispx', 'per_dispy', 'per_dispz',
         'per_imagx', 'per_imagy', 'per_imagz', 'freq', 'amp', 'nodal_diam',
         'pass_number', 'fwd', 'aero', 'cmplx', 'norm', 'method', 'uds_bc',
         'uds', 'gtemp_bc', 'g_temperature', 'g_qflux',
         'wall_restitution_coeff', 'omega', 'rotation_axis_origin',
         'rotation_axis_direction', 'adhesion_angle', 'specified_shear',
         'shear_stress', 'fslip', 'eslip', 'surf_tens_grad',
         'contact_resistance', 'reaction_mechs', 'surf_washcoat_factor',
         'initial_deposition_height', 'solid_species_density',
         'ablation_select_model', 'ablation_vielle_a', 'ablation_vielle_n',
         'ablation_flux', 'ablation_surfacerxn_density',
         'ablation_species_mf', 'specular_coeff', 'mom_accom_coef',
         'therm_accom_coef', 'eve_accom_coef', 'film_wall', 'film_wall_bc',
         'film_height', 'flux_momentum', 'film_relative_vel',
         'film_bc_imp_press', 'film_temperature', 'film_scalar',
         'film_source', 'film_h_src', 'momentum_source', 'film_t_src',
         'film_s_src', 'film_phase_change', 'film_phase_change_model',
         'film_cond_const', 'film_vapo_const', 'film_cond_rate',
         'film_vapo_rate', 'film_momentum_coupling', 'film_splash_wall',
         'film_boundary_separation', 'film_impinge_model',
         'film_splash_nparc', 'film_crit_temp_factor', 'film_roughness_ra',
         'film_roughness_rz', 'film_upper_deposition_limit_offset',
         'film_deposition_delta_t', 'film_laplace_number_constant',
         'film_partial_evap_ratio', 'film_contact_angle',
         'film_contact_angle_mean', 'film_contact_angle_rstd',
         'film_contact_angle_beta', 'film_vof_coupling_high',
         'film_vof_trans_high', 'film_vof_trans_high_relax',
         'film_vof_coupling_low', 'film_vof_trans_low',
         'film_vof_trans_low_relax', 'caf', 'thermal_stabilization',
         'scale_factor', 'stab_method', 'fensapice_flow_bc_subtype',
         'fensapice_ice_icing_mode', 'fensapice_ice_hflux',
         'fensapice_ice_hflux_1', 'fensapice_drop_vwet']

    _child_classes = dict(
        geom_disable=geom_disable_cls,
        geom_dir_spec=geom_dir_spec_cls,
        geom_dir_x=geom_dir_x_cls,
        geom_dir_y=geom_dir_y_cls,
        geom_dir_z=geom_dir_z_cls,
        geom_levels=geom_levels_cls,
        geom_bgthread=geom_bgthread_cls,
        d=d_cls,
        q_dot=q_dot_cls,
        material=material_cls,
        thermal_bc=thermal_bc_cls,
        t=t_cls,
        q=q_cls,
        h=h_cls,
        tinf=tinf_cls,
        planar_conduction=planar_conduction_cls,
        shell_conduction=shell_conduction_cls,
        thin_wall=thin_wall_cls,
        motion_bc=motion_bc_cls,
        shear_bc=shear_bc_cls,
        rough_bc=rough_bc_cls,
        moving=moving_cls,
        relative=relative_cls,
        rotating=rotating_cls,
        vmag=vmag_cls,
        wall_translation=wall_translation_cls,
        components=components_cls,
        velocity=velocity_cls,
        in_emiss=in_emiss_cls,
        ex_emiss=ex_emiss_cls,
        trad=trad_cls,
        int_rad=int_rad_cls,
        trad_internal=trad_internal_cls,
        area_enhancement_factor=area_enhancement_factor_cls,
        rough_option=rough_option_cls,
        rough_nasa=rough_nasa_cls,
        rough_shin_et_al=rough_shin_et_al_cls,
        rough_data=rough_data_cls,
        roughness_height=roughness_height_cls,
        roughness_const=roughness_const_cls,
        roughness_height_cp=roughness_height_cp_cls,
        roughness_const_cp=roughness_const_cp_cls,
        roughness_const_nasa=roughness_const_nasa_cls,
        roughness_const_shin=roughness_const_shin_cls,
        roughness_const_data=roughness_const_data_cls,
        variable_roughness=variable_roughness_cls,
        free_stream_velocity=free_stream_velocity_cls,
        free_stream_temp=free_stream_temp_cls,
        characteristic_length=characteristic_length_cls,
        free_stream_temp_cp=free_stream_temp_cp_cls,
        characteristic_length_cp=characteristic_length_cp_cls,
        liquid_content=liquid_content_cls,
        liquid_content_cp=liquid_content_cp_cls,
        droplet_diameter=droplet_diameter_cls,
        dpm_bc_type=dpm_bc_type_cls,
        dpm_bc_collision_partner=dpm_bc_collision_partner_cls,
        reinj_inj=reinj_inj_cls,
        dpm_bc_norm_coeff=dpm_bc_norm_coeff_cls,
        dpm_bc_tang_coeff=dpm_bc_tang_coeff_cls,
        dpm_bc_frictn_coeff=dpm_bc_frictn_coeff_cls,
        dpm_bc_udf=dpm_bc_udf_cls,
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
        dpm_bc_erosion_generic=dpm_bc_erosion_generic_cls,
        dpm_bc_erosion=dpm_bc_erosion_cls,
        dpm_bc_erosion_c=dpm_bc_erosion_c_cls,
        dpm_bc_erosion_n=dpm_bc_erosion_n_cls,
        dpm_bc_erosion_finnie=dpm_bc_erosion_finnie_cls,
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
        band_in_emiss=band_in_emiss_cls,
        radiation_bc=radiation_bc_cls,
        mc_bsource_p=mc_bsource_p_cls,
        mc_poldfun_p=mc_poldfun_p_cls,
        polar_func_type=polar_func_type_cls,
        mc_polar_expr=mc_polar_expr_cls,
        polar_pair_list=polar_pair_list_cls,
        pold_pair_list_rad=pold_pair_list_rad_cls,
        radiation_direction=radiation_direction_cls,
        coll_dtheta=coll_dtheta_cls,
        coll_dphi=coll_dphi_cls,
        band_q_irrad=band_q_irrad_cls,
        band_q_irrad_diffuse=band_q_irrad_diffuse_cls,
        band_diffuse_frac=band_diffuse_frac_cls,
        radiating_s2s_surface=radiating_s2s_surface_cls,
        critical_zone=critical_zone_cls,
        fpsc=fpsc_cls,
        parallel_collimated_beam=parallel_collimated_beam_cls,
        solar_fluxes=solar_fluxes_cls,
        solar_direction=solar_direction_cls,
        solar_irradiation=solar_irradiation_cls,
        v_transmissivity=v_transmissivity_cls,
        ir_transmissivity=ir_transmissivity_cls,
        v_opq_absorbtivity=v_opq_absorbtivity_cls,
        ir_opq_absorbtivity=ir_opq_absorbtivity_cls,
        v_st_absorbtivity=v_st_absorbtivity_cls,
        ir_st_absorbtivity=ir_st_absorbtivity_cls,
        d_st_absorbtivity=d_st_absorbtivity_cls,
        d_transmissivity=d_transmissivity_cls,
        fsi_interface=fsi_interface_cls,
        react=react_cls,
        partially_catalytic=partially_catalytic_cls,
        partially_catalytic_material=partially_catalytic_material_cls,
        partially_catalytic_recombination_coefficient_o=partially_catalytic_recombination_coefficient_o_cls,
        partially_catalytic_recombination_coefficient_n=partially_catalytic_recombination_coefficient_n_cls,
        partially_catalytic_recombination_model=partially_catalytic_recombination_model_cls,
        species_spec=species_spec_cls,
        mf=mf_cls,
        elec_potential_type=elec_potential_type_cls,
        potential_value=potential_value_cls,
        elec_potential_jump=elec_potential_jump_cls,
        elec_potential_resistance=elec_potential_resistance_cls,
        dual_potential_type=dual_potential_type_cls,
        dual_potential_value=dual_potential_value_cls,
        echem_reaction=echem_reaction_cls,
        elec_potential_mechs=elec_potential_mechs_cls,
        faradaic_heat=faradaic_heat_cls,
        li_ion_type=li_ion_type_cls,
        li_ion_value=li_ion_value_cls,
        x_displacement_type=x_displacement_type_cls,
        x_displacement_value=x_displacement_value_cls,
        y_displacement_type=y_displacement_type_cls,
        y_displacement_value=y_displacement_value_cls,
        z_displacement_type=z_displacement_type_cls,
        z_displacement_value=z_displacement_value_cls,
        per_dispx=per_dispx_cls,
        per_dispy=per_dispy_cls,
        per_dispz=per_dispz_cls,
        per_imagx=per_imagx_cls,
        per_imagy=per_imagy_cls,
        per_imagz=per_imagz_cls,
        freq=freq_cls,
        amp=amp_cls,
        nodal_diam=nodal_diam_cls,
        pass_number=pass_number_cls,
        fwd=fwd_cls,
        aero=aero_cls,
        cmplx=cmplx_cls,
        norm=norm_cls,
        method=method_cls,
        uds_bc=uds_bc_cls,
        uds=uds_cls,
        gtemp_bc=gtemp_bc_cls,
        g_temperature=g_temperature_cls,
        g_qflux=g_qflux_cls,
        wall_restitution_coeff=wall_restitution_coeff_cls,
        omega=omega_cls,
        rotation_axis_origin=rotation_axis_origin_cls,
        rotation_axis_direction=rotation_axis_direction_cls,
        adhesion_angle=adhesion_angle_cls,
        specified_shear=specified_shear_cls,
        shear_stress=shear_stress_cls,
        fslip=fslip_cls,
        eslip=eslip_cls,
        surf_tens_grad=surf_tens_grad_cls,
        contact_resistance=contact_resistance_cls,
        reaction_mechs=reaction_mechs_cls,
        surf_washcoat_factor=surf_washcoat_factor_cls,
        initial_deposition_height=initial_deposition_height_cls,
        solid_species_density=solid_species_density_cls,
        ablation_select_model=ablation_select_model_cls,
        ablation_vielle_a=ablation_vielle_a_cls,
        ablation_vielle_n=ablation_vielle_n_cls,
        ablation_flux=ablation_flux_cls,
        ablation_surfacerxn_density=ablation_surfacerxn_density_cls,
        ablation_species_mf=ablation_species_mf_cls,
        specular_coeff=specular_coeff_cls,
        mom_accom_coef=mom_accom_coef_cls,
        therm_accom_coef=therm_accom_coef_cls,
        eve_accom_coef=eve_accom_coef_cls,
        film_wall=film_wall_cls,
        film_wall_bc=film_wall_bc_cls,
        film_height=film_height_cls,
        flux_momentum=flux_momentum_cls,
        film_relative_vel=film_relative_vel_cls,
        film_bc_imp_press=film_bc_imp_press_cls,
        film_temperature=film_temperature_cls,
        film_scalar=film_scalar_cls,
        film_source=film_source_cls,
        film_h_src=film_h_src_cls,
        momentum_source=momentum_source_cls,
        film_t_src=film_t_src_cls,
        film_s_src=film_s_src_cls,
        film_phase_change=film_phase_change_cls,
        film_phase_change_model=film_phase_change_model_cls,
        film_cond_const=film_cond_const_cls,
        film_vapo_const=film_vapo_const_cls,
        film_cond_rate=film_cond_rate_cls,
        film_vapo_rate=film_vapo_rate_cls,
        film_momentum_coupling=film_momentum_coupling_cls,
        film_splash_wall=film_splash_wall_cls,
        film_boundary_separation=film_boundary_separation_cls,
        film_impinge_model=film_impinge_model_cls,
        film_splash_nparc=film_splash_nparc_cls,
        film_crit_temp_factor=film_crit_temp_factor_cls,
        film_roughness_ra=film_roughness_ra_cls,
        film_roughness_rz=film_roughness_rz_cls,
        film_upper_deposition_limit_offset=film_upper_deposition_limit_offset_cls,
        film_deposition_delta_t=film_deposition_delta_t_cls,
        film_laplace_number_constant=film_laplace_number_constant_cls,
        film_partial_evap_ratio=film_partial_evap_ratio_cls,
        film_contact_angle=film_contact_angle_cls,
        film_contact_angle_mean=film_contact_angle_mean_cls,
        film_contact_angle_rstd=film_contact_angle_rstd_cls,
        film_contact_angle_beta=film_contact_angle_beta_cls,
        film_vof_coupling_high=film_vof_coupling_high_cls,
        film_vof_trans_high=film_vof_trans_high_cls,
        film_vof_trans_high_relax=film_vof_trans_high_relax_cls,
        film_vof_coupling_low=film_vof_coupling_low_cls,
        film_vof_trans_low=film_vof_trans_low_cls,
        film_vof_trans_low_relax=film_vof_trans_low_relax_cls,
        caf=caf_cls,
        thermal_stabilization=thermal_stabilization_cls,
        scale_factor=scale_factor_cls,
        stab_method=stab_method_cls,
        fensapice_flow_bc_subtype=fensapice_flow_bc_subtype_cls,
        fensapice_ice_icing_mode=fensapice_ice_icing_mode_cls,
        fensapice_ice_hflux=fensapice_ice_hflux_cls,
        fensapice_ice_hflux_1=fensapice_ice_hflux_1_cls,
        fensapice_drop_vwet=fensapice_drop_vwet_cls,
    )

