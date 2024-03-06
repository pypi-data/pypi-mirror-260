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

from .phase_3 import phase as phase_cls
from .geom_disable import geom_disable as geom_disable_cls
from .geom_dir_spec import geom_dir_spec as geom_dir_spec_cls
from .geom_dir_x import geom_dir_x as geom_dir_x_cls
from .geom_dir_y import geom_dir_y as geom_dir_y_cls
from .geom_dir_z import geom_dir_z as geom_dir_z_cls
from .geom_levels import geom_levels as geom_levels_cls
from .geom_bgthread import geom_bgthread as geom_bgthread_cls
from .open_channel import open_channel as open_channel_cls
from .outlet_number import outlet_number as outlet_number_cls
from .pressure_spec_method import pressure_spec_method as pressure_spec_method_cls
from .press_spec import press_spec as press_spec_cls
from .frame_of_reference import frame_of_reference as frame_of_reference_cls
from .phase_spec import phase_spec as phase_spec_cls
from .ht_local import ht_local as ht_local_cls
from .p import p as p_cls
from .p_profile_multiplier import p_profile_multiplier as p_profile_multiplier_cls
from .ht_bottom import ht_bottom as ht_bottom_cls
from .den_spec import den_spec as den_spec_cls
from .t0 import t0 as t0_cls
from .direction_spec import direction_spec as direction_spec_cls
from .coordinate_system import coordinate_system as coordinate_system_cls
from .flow_direction_component import flow_direction_component as flow_direction_component_cls
from .axis_direction_component_1 import axis_direction_component as axis_direction_component_cls
from .axis_origin_component_1 import axis_origin_component as axis_origin_component_cls
from .ke_spec import ke_spec as ke_spec_cls
from .nut import nut as nut_cls
from .kl import kl as kl_cls
from .intermit import intermit as intermit_cls
from .k import k as k_cls
from .e import e as e_cls
from .o import o as o_cls
from .v2 import v2 as v2_cls
from .turb_intensity import turb_intensity as turb_intensity_cls
from .turb_length_scale import turb_length_scale as turb_length_scale_cls
from .turb_hydraulic_diam import turb_hydraulic_diam as turb_hydraulic_diam_cls
from .turb_viscosity_ratio import turb_viscosity_ratio as turb_viscosity_ratio_cls
from .turb_viscosity_ratio_profile import turb_viscosity_ratio_profile as turb_viscosity_ratio_profile_cls
from .rst_spec import rst_spec as rst_spec_cls
from .uu import uu as uu_cls
from .vv import vv as vv_cls
from .ww import ww as ww_cls
from .uv import uv as uv_cls
from .vw import vw as vw_cls
from .uw import uw as uw_cls
from .ksgs_spec import ksgs_spec as ksgs_spec_cls
from .ksgs import ksgs as ksgs_cls
from .sgs_turb_intensity import sgs_turb_intensity as sgs_turb_intensity_cls
from .radiation_bc import radiation_bc as radiation_bc_cls
from .radial_direction_component import radial_direction_component as radial_direction_component_cls
from .coll_dtheta import coll_dtheta as coll_dtheta_cls
from .coll_dphi import coll_dphi as coll_dphi_cls
from .band_q_irrad import band_q_irrad as band_q_irrad_cls
from .band_q_irrad_diffuse import band_q_irrad_diffuse as band_q_irrad_diffuse_cls
from .parallel_collimated_beam import parallel_collimated_beam as parallel_collimated_beam_cls
from .solar_direction import solar_direction as solar_direction_cls
from .solar_irradiation import solar_irradiation as solar_irradiation_cls
from .t_b_b_spec import t_b_b_spec as t_b_b_spec_cls
from .t_b_b import t_b_b as t_b_b_cls
from .in_emiss import in_emiss as in_emiss_cls
from .fmean import fmean as fmean_cls
from .fmean2 import fmean2 as fmean2_cls
from .fvar import fvar as fvar_cls
from .fvar2 import fvar2 as fvar2_cls
from .granular_temperature import granular_temperature as granular_temperature_cls
from .iac import iac as iac_cls
from .lsfun import lsfun as lsfun_cls
from .vof_spec import vof_spec as vof_spec_cls
from .volume_fraction import volume_fraction as volume_fraction_cls
from .species_in_mole_fractions import species_in_mole_fractions as species_in_mole_fractions_cls
from .mf import mf as mf_cls
from .elec_potential_type import elec_potential_type as elec_potential_type_cls
from .potential_value import potential_value as potential_value_cls
from .dual_potential_type import dual_potential_type as dual_potential_type_cls
from .dual_potential_value import dual_potential_value as dual_potential_value_cls
from .x_displacement_type import x_displacement_type as x_displacement_type_cls
from .x_displacement_value import x_displacement_value as x_displacement_value_cls
from .y_displacement_type import y_displacement_type as y_displacement_type_cls
from .y_displacement_value import y_displacement_value as y_displacement_value_cls
from .z_displacement_type import z_displacement_type as z_displacement_type_cls
from .z_displacement_value import z_displacement_value as z_displacement_value_cls
from .prob_mode_1 import prob_mode_1 as prob_mode_1_cls
from .prob_mode_2 import prob_mode_2 as prob_mode_2_cls
from .prob_mode_3 import prob_mode_3 as prob_mode_3_cls
from .premixc import premixc as premixc_cls
from .premixc_var import premixc_var as premixc_var_cls
from .ecfm_sigma import ecfm_sigma as ecfm_sigma_cls
from .inert import inert as inert_cls
from .pollut_no import pollut_no as pollut_no_cls
from .pollut_hcn import pollut_hcn as pollut_hcn_cls
from .pollut_nh3 import pollut_nh3 as pollut_nh3_cls
from .pollut_n2o import pollut_n2o as pollut_n2o_cls
from .pollut_urea import pollut_urea as pollut_urea_cls
from .pollut_hnco import pollut_hnco as pollut_hnco_cls
from .pollut_nco import pollut_nco as pollut_nco_cls
from .pollut_so2 import pollut_so2 as pollut_so2_cls
from .pollut_h2s import pollut_h2s as pollut_h2s_cls
from .pollut_so3 import pollut_so3 as pollut_so3_cls
from .pollut_sh import pollut_sh as pollut_sh_cls
from .pollut_so import pollut_so as pollut_so_cls
from .pollut_soot import pollut_soot as pollut_soot_cls
from .pollut_nuclei import pollut_nuclei as pollut_nuclei_cls
from .pollut_ctar import pollut_ctar as pollut_ctar_cls
from .pollut_hg import pollut_hg as pollut_hg_cls
from .pollut_hgcl2 import pollut_hgcl2 as pollut_hgcl2_cls
from .pollut_hcl import pollut_hcl as pollut_hcl_cls
from .pollut_hgo import pollut_hgo as pollut_hgo_cls
from .pollut_cl import pollut_cl as pollut_cl_cls
from .pollut_cl2 import pollut_cl2 as pollut_cl2_cls
from .pollut_hgcl import pollut_hgcl as pollut_hgcl_cls
from .pollut_hocl import pollut_hocl as pollut_hocl_cls
from .tss_scalar import tss_scalar as tss_scalar_cls
from .fensapice_flow_bc_subtype import fensapice_flow_bc_subtype as fensapice_flow_bc_subtype_cls
from .uds_bc import uds_bc as uds_bc_cls
from .uds import uds as uds_cls
from .pb_disc_bc import pb_disc_bc as pb_disc_bc_cls
from .pb_disc import pb_disc as pb_disc_cls
from .pb_qmom_bc import pb_qmom_bc as pb_qmom_bc_cls
from .pb_qmom import pb_qmom as pb_qmom_cls
from .pb_smm_bc import pb_smm_bc as pb_smm_bc_cls
from .pb_smm import pb_smm as pb_smm_cls
from .pb_dqmom_bc import pb_dqmom_bc as pb_dqmom_bc_cls
from .pb_dqmom import pb_dqmom as pb_dqmom_cls
from .dpm_bc_type import dpm_bc_type as dpm_bc_type_cls
from .dpm_bc_collision_partner import dpm_bc_collision_partner as dpm_bc_collision_partner_cls
from .reinj_inj import reinj_inj as reinj_inj_cls
from .dpm_bc_udf import dpm_bc_udf as dpm_bc_udf_cls
from .mixing_plane_thread import mixing_plane_thread as mixing_plane_thread_cls
from .ac_options import ac_options as ac_options_cls
from .p_backflow_spec import p_backflow_spec as p_backflow_spec_cls
from .p_backflow_spec_gen import p_backflow_spec_gen as p_backflow_spec_gen_cls
from .impedance_0 import impedance_0 as impedance_0_cls
from .impedance_1 import impedance_1 as impedance_1_cls
from .impedance_2 import impedance_2 as impedance_2_cls
from .ac_wave import ac_wave as ac_wave_cls
from .prevent_reverse_flow import prevent_reverse_flow as prevent_reverse_flow_cls
from .radial import radial as radial_cls
from .avg_press_spec import avg_press_spec as avg_press_spec_cls
from .press_averaging_method import press_averaging_method as press_averaging_method_cls
from .targeted_mf_boundary import targeted_mf_boundary as targeted_mf_boundary_cls
from .targeted_mf import targeted_mf as targeted_mf_cls
from .targeted_mf_pmax import targeted_mf_pmax as targeted_mf_pmax_cls
from .targeted_mf_pmin import targeted_mf_pmin as targeted_mf_pmin_cls
from .gen_nrbc_spec import gen_nrbc_spec as gen_nrbc_spec_cls
from .wsf import wsf as wsf_cls
from .wsb import wsb as wsb_cls
from .wsn import wsn as wsn_cls
from .solar_fluxes import solar_fluxes as solar_fluxes_cls
from .solar_shining_factor import solar_shining_factor as solar_shining_factor_cls
from .radiating_s2s_surface import radiating_s2s_surface as radiating_s2s_surface_cls
from .a import a as a_cls
from .strength import strength as strength_cls
from .new_fan_definition import new_fan_definition as new_fan_definition_cls
class exhaust_fan_child(Group):
    """
    'child_object_type' of exhaust_fan.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['phase', 'geom_disable', 'geom_dir_spec', 'geom_dir_x', 'geom_dir_y',
         'geom_dir_z', 'geom_levels', 'geom_bgthread', 'open_channel',
         'outlet_number', 'pressure_spec_method', 'press_spec',
         'frame_of_reference', 'phase_spec', 'ht_local', 'p',
         'p_profile_multiplier', 'ht_bottom', 'den_spec', 't0',
         'direction_spec', 'coordinate_system', 'flow_direction_component',
         'axis_direction_component', 'axis_origin_component', 'ke_spec',
         'nut', 'kl', 'intermit', 'k', 'e', 'o', 'v2', 'turb_intensity',
         'turb_length_scale', 'turb_hydraulic_diam', 'turb_viscosity_ratio',
         'turb_viscosity_ratio_profile', 'rst_spec', 'uu', 'vv', 'ww', 'uv',
         'vw', 'uw', 'ksgs_spec', 'ksgs', 'sgs_turb_intensity',
         'radiation_bc', 'radial_direction_component', 'coll_dtheta',
         'coll_dphi', 'band_q_irrad', 'band_q_irrad_diffuse',
         'parallel_collimated_beam', 'solar_direction', 'solar_irradiation',
         't_b_b_spec', 't_b_b', 'in_emiss', 'fmean', 'fmean2', 'fvar',
         'fvar2', 'granular_temperature', 'iac', 'lsfun', 'vof_spec',
         'volume_fraction', 'species_in_mole_fractions', 'mf',
         'elec_potential_type', 'potential_value', 'dual_potential_type',
         'dual_potential_value', 'x_displacement_type',
         'x_displacement_value', 'y_displacement_type',
         'y_displacement_value', 'z_displacement_type',
         'z_displacement_value', 'prob_mode_1', 'prob_mode_2', 'prob_mode_3',
         'premixc', 'premixc_var', 'ecfm_sigma', 'inert', 'pollut_no',
         'pollut_hcn', 'pollut_nh3', 'pollut_n2o', 'pollut_urea',
         'pollut_hnco', 'pollut_nco', 'pollut_so2', 'pollut_h2s',
         'pollut_so3', 'pollut_sh', 'pollut_so', 'pollut_soot',
         'pollut_nuclei', 'pollut_ctar', 'pollut_hg', 'pollut_hgcl2',
         'pollut_hcl', 'pollut_hgo', 'pollut_cl', 'pollut_cl2', 'pollut_hgcl',
         'pollut_hocl', 'tss_scalar', 'fensapice_flow_bc_subtype', 'uds_bc',
         'uds', 'pb_disc_bc', 'pb_disc', 'pb_qmom_bc', 'pb_qmom', 'pb_smm_bc',
         'pb_smm', 'pb_dqmom_bc', 'pb_dqmom', 'dpm_bc_type',
         'dpm_bc_collision_partner', 'reinj_inj', 'dpm_bc_udf',
         'mixing_plane_thread', 'ac_options', 'p_backflow_spec',
         'p_backflow_spec_gen', 'impedance_0', 'impedance_1', 'impedance_2',
         'ac_wave', 'prevent_reverse_flow', 'radial', 'avg_press_spec',
         'press_averaging_method', 'targeted_mf_boundary', 'targeted_mf',
         'targeted_mf_pmax', 'targeted_mf_pmin', 'gen_nrbc_spec', 'wsf',
         'wsb', 'wsn', 'solar_fluxes', 'solar_shining_factor',
         'radiating_s2s_surface', 'a', 'strength', 'new_fan_definition']

    _child_classes = dict(
        phase=phase_cls,
        geom_disable=geom_disable_cls,
        geom_dir_spec=geom_dir_spec_cls,
        geom_dir_x=geom_dir_x_cls,
        geom_dir_y=geom_dir_y_cls,
        geom_dir_z=geom_dir_z_cls,
        geom_levels=geom_levels_cls,
        geom_bgthread=geom_bgthread_cls,
        open_channel=open_channel_cls,
        outlet_number=outlet_number_cls,
        pressure_spec_method=pressure_spec_method_cls,
        press_spec=press_spec_cls,
        frame_of_reference=frame_of_reference_cls,
        phase_spec=phase_spec_cls,
        ht_local=ht_local_cls,
        p=p_cls,
        p_profile_multiplier=p_profile_multiplier_cls,
        ht_bottom=ht_bottom_cls,
        den_spec=den_spec_cls,
        t0=t0_cls,
        direction_spec=direction_spec_cls,
        coordinate_system=coordinate_system_cls,
        flow_direction_component=flow_direction_component_cls,
        axis_direction_component=axis_direction_component_cls,
        axis_origin_component=axis_origin_component_cls,
        ke_spec=ke_spec_cls,
        nut=nut_cls,
        kl=kl_cls,
        intermit=intermit_cls,
        k=k_cls,
        e=e_cls,
        o=o_cls,
        v2=v2_cls,
        turb_intensity=turb_intensity_cls,
        turb_length_scale=turb_length_scale_cls,
        turb_hydraulic_diam=turb_hydraulic_diam_cls,
        turb_viscosity_ratio=turb_viscosity_ratio_cls,
        turb_viscosity_ratio_profile=turb_viscosity_ratio_profile_cls,
        rst_spec=rst_spec_cls,
        uu=uu_cls,
        vv=vv_cls,
        ww=ww_cls,
        uv=uv_cls,
        vw=vw_cls,
        uw=uw_cls,
        ksgs_spec=ksgs_spec_cls,
        ksgs=ksgs_cls,
        sgs_turb_intensity=sgs_turb_intensity_cls,
        radiation_bc=radiation_bc_cls,
        radial_direction_component=radial_direction_component_cls,
        coll_dtheta=coll_dtheta_cls,
        coll_dphi=coll_dphi_cls,
        band_q_irrad=band_q_irrad_cls,
        band_q_irrad_diffuse=band_q_irrad_diffuse_cls,
        parallel_collimated_beam=parallel_collimated_beam_cls,
        solar_direction=solar_direction_cls,
        solar_irradiation=solar_irradiation_cls,
        t_b_b_spec=t_b_b_spec_cls,
        t_b_b=t_b_b_cls,
        in_emiss=in_emiss_cls,
        fmean=fmean_cls,
        fmean2=fmean2_cls,
        fvar=fvar_cls,
        fvar2=fvar2_cls,
        granular_temperature=granular_temperature_cls,
        iac=iac_cls,
        lsfun=lsfun_cls,
        vof_spec=vof_spec_cls,
        volume_fraction=volume_fraction_cls,
        species_in_mole_fractions=species_in_mole_fractions_cls,
        mf=mf_cls,
        elec_potential_type=elec_potential_type_cls,
        potential_value=potential_value_cls,
        dual_potential_type=dual_potential_type_cls,
        dual_potential_value=dual_potential_value_cls,
        x_displacement_type=x_displacement_type_cls,
        x_displacement_value=x_displacement_value_cls,
        y_displacement_type=y_displacement_type_cls,
        y_displacement_value=y_displacement_value_cls,
        z_displacement_type=z_displacement_type_cls,
        z_displacement_value=z_displacement_value_cls,
        prob_mode_1=prob_mode_1_cls,
        prob_mode_2=prob_mode_2_cls,
        prob_mode_3=prob_mode_3_cls,
        premixc=premixc_cls,
        premixc_var=premixc_var_cls,
        ecfm_sigma=ecfm_sigma_cls,
        inert=inert_cls,
        pollut_no=pollut_no_cls,
        pollut_hcn=pollut_hcn_cls,
        pollut_nh3=pollut_nh3_cls,
        pollut_n2o=pollut_n2o_cls,
        pollut_urea=pollut_urea_cls,
        pollut_hnco=pollut_hnco_cls,
        pollut_nco=pollut_nco_cls,
        pollut_so2=pollut_so2_cls,
        pollut_h2s=pollut_h2s_cls,
        pollut_so3=pollut_so3_cls,
        pollut_sh=pollut_sh_cls,
        pollut_so=pollut_so_cls,
        pollut_soot=pollut_soot_cls,
        pollut_nuclei=pollut_nuclei_cls,
        pollut_ctar=pollut_ctar_cls,
        pollut_hg=pollut_hg_cls,
        pollut_hgcl2=pollut_hgcl2_cls,
        pollut_hcl=pollut_hcl_cls,
        pollut_hgo=pollut_hgo_cls,
        pollut_cl=pollut_cl_cls,
        pollut_cl2=pollut_cl2_cls,
        pollut_hgcl=pollut_hgcl_cls,
        pollut_hocl=pollut_hocl_cls,
        tss_scalar=tss_scalar_cls,
        fensapice_flow_bc_subtype=fensapice_flow_bc_subtype_cls,
        uds_bc=uds_bc_cls,
        uds=uds_cls,
        pb_disc_bc=pb_disc_bc_cls,
        pb_disc=pb_disc_cls,
        pb_qmom_bc=pb_qmom_bc_cls,
        pb_qmom=pb_qmom_cls,
        pb_smm_bc=pb_smm_bc_cls,
        pb_smm=pb_smm_cls,
        pb_dqmom_bc=pb_dqmom_bc_cls,
        pb_dqmom=pb_dqmom_cls,
        dpm_bc_type=dpm_bc_type_cls,
        dpm_bc_collision_partner=dpm_bc_collision_partner_cls,
        reinj_inj=reinj_inj_cls,
        dpm_bc_udf=dpm_bc_udf_cls,
        mixing_plane_thread=mixing_plane_thread_cls,
        ac_options=ac_options_cls,
        p_backflow_spec=p_backflow_spec_cls,
        p_backflow_spec_gen=p_backflow_spec_gen_cls,
        impedance_0=impedance_0_cls,
        impedance_1=impedance_1_cls,
        impedance_2=impedance_2_cls,
        ac_wave=ac_wave_cls,
        prevent_reverse_flow=prevent_reverse_flow_cls,
        radial=radial_cls,
        avg_press_spec=avg_press_spec_cls,
        press_averaging_method=press_averaging_method_cls,
        targeted_mf_boundary=targeted_mf_boundary_cls,
        targeted_mf=targeted_mf_cls,
        targeted_mf_pmax=targeted_mf_pmax_cls,
        targeted_mf_pmin=targeted_mf_pmin_cls,
        gen_nrbc_spec=gen_nrbc_spec_cls,
        wsf=wsf_cls,
        wsb=wsb_cls,
        wsn=wsn_cls,
        solar_fluxes=solar_fluxes_cls,
        solar_shining_factor=solar_shining_factor_cls,
        radiating_s2s_surface=radiating_s2s_surface_cls,
        a=a_cls,
        strength=strength_cls,
        new_fan_definition=new_fan_definition_cls,
    )

