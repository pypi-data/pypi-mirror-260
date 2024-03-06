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

from .porous import porous as porous_cls
from .cursys_name import cursys_name as cursys_name_cls
from .dir_spec_cond import dir_spec_cond as dir_spec_cond_cls
from .direction_1_vector import direction_1_vector as direction_1_vector_cls
from .direction_2_vector import direction_2_vector as direction_2_vector_cls
from .cone_axis_vector import cone_axis_vector as cone_axis_vector_cls
from .point_on_cone_axis import point_on_cone_axis as point_on_cone_axis_cls
from .cone_angle import cone_angle as cone_angle_cls
from .rel_vel_resistance import rel_vel_resistance as rel_vel_resistance_cls
from .viscous_resistance import viscous_resistance as viscous_resistance_cls
from .alt_inertial_form import alt_inertial_form as alt_inertial_form_cls
from .inertial_resistance import inertial_resistance as inertial_resistance_cls
from .power_law_c0 import power_law_c0 as power_law_c0_cls
from .power_law_c1 import power_law_c1 as power_law_c1_cls
from .porosity import porosity as porosity_cls
from .relative_viscosity import relative_viscosity as relative_viscosity_cls
from .none import none as none_cls
from .corey import corey as corey_cls
from .stone_1 import stone_1 as stone_1_cls
from .stone_2 import stone_2 as stone_2_cls
from .rel_perm_limit_p1 import rel_perm_limit_p1 as rel_perm_limit_p1_cls
from .rel_perm_limit_p2 import rel_perm_limit_p2 as rel_perm_limit_p2_cls
from .ref_perm_p1 import ref_perm_p1 as ref_perm_p1_cls
from .exp_p1 import exp_p1 as exp_p1_cls
from .res_sat_p1 import res_sat_p1 as res_sat_p1_cls
from .ref_perm_p2 import ref_perm_p2 as ref_perm_p2_cls
from .exp_p2 import exp_p2 as exp_p2_cls
from .res_sat_p2 import res_sat_p2 as res_sat_p2_cls
from .ref_perm_p3 import ref_perm_p3 as ref_perm_p3_cls
from .exp_p3 import exp_p3 as exp_p3_cls
from .res_sat_p3 import res_sat_p3 as res_sat_p3_cls
from .capillary_pressure_1 import capillary_pressure as capillary_pressure_cls
from .max_capillary_pressure import max_capillary_pressure as max_capillary_pressure_cls
from .van_genuchten_pg import van_genuchten_pg as van_genuchten_pg_cls
from .van_genuchten_ng import van_genuchten_ng as van_genuchten_ng_cls
from .skjaeveland_nw_pc_coef import skjaeveland_nw_pc_coef as skjaeveland_nw_pc_coef_cls
from .skjaeveland_nw_pc_pwr import skjaeveland_nw_pc_pwr as skjaeveland_nw_pc_pwr_cls
from .skjaeveland_wet_pc_coef import skjaeveland_wet_pc_coef as skjaeveland_wet_pc_coef_cls
from .skjaeveland_wet_pc_pwr import skjaeveland_wet_pc_pwr as skjaeveland_wet_pc_pwr_cls
from .brooks_corey_pe import brooks_corey_pe as brooks_corey_pe_cls
from .brooks_corey_ng import brooks_corey_ng as brooks_corey_ng_cls
from .leverett_con_ang import leverett_con_ang as leverett_con_ang_cls
from .rp_cbox_p1 import rp_cbox_p1 as rp_cbox_p1_cls
from .rp_edit_p1 import rp_edit_p1 as rp_edit_p1_cls
from .rel_perm_tabular_p1 import rel_perm_tabular_p1 as rel_perm_tabular_p1_cls
from .rel_perm_table_p1 import rel_perm_table_p1 as rel_perm_table_p1_cls
from .rel_perm_satw_p1 import rel_perm_satw_p1 as rel_perm_satw_p1_cls
from .rel_perm_rp_p1 import rel_perm_rp_p1 as rel_perm_rp_p1_cls
from .rp_cbox_p2 import rp_cbox_p2 as rp_cbox_p2_cls
from .rp_edit_p2 import rp_edit_p2 as rp_edit_p2_cls
from .rel_perm_tabular_p2 import rel_perm_tabular_p2 as rel_perm_tabular_p2_cls
from .rel_perm_table_p2 import rel_perm_table_p2 as rel_perm_table_p2_cls
from .rel_perm_satw_p2 import rel_perm_satw_p2 as rel_perm_satw_p2_cls
from .rel_perm_rp_p2 import rel_perm_rp_p2 as rel_perm_rp_p2_cls
from .wetting_phase import wetting_phase as wetting_phase_cls
from .non_wetting_phase import non_wetting_phase as non_wetting_phase_cls
from .equib_thermal import equib_thermal as equib_thermal_cls
from .non_equib_thermal import non_equib_thermal as non_equib_thermal_cls
from .solid_material import solid_material as solid_material_cls
from .area_density import area_density as area_density_cls
from .heat_transfer_coeff import heat_transfer_coeff as heat_transfer_coeff_cls
from .porous_structure import porous_structure as porous_structure_cls
from .structure_material import structure_material as structure_material_cls
from .anisotropic_spe_diff import anisotropic_spe_diff as anisotropic_spe_diff_cls
from .spe_diff_xx import spe_diff_xx as spe_diff_xx_cls
from .spe_diff_xy import spe_diff_xy as spe_diff_xy_cls
from .spe_diff_xz import spe_diff_xz as spe_diff_xz_cls
from .spe_diff_yx import spe_diff_yx as spe_diff_yx_cls
from .spe_diff_yy import spe_diff_yy as spe_diff_yy_cls
from .spe_diff_yz import spe_diff_yz as spe_diff_yz_cls
from .spe_diff_zx import spe_diff_zx as spe_diff_zx_cls
from .spe_diff_zy import spe_diff_zy as spe_diff_zy_cls
from .spe_diff_zz import spe_diff_zz as spe_diff_zz_cls
class porous_zone(Group):
    """
    Help not available.
    """

    fluent_name = "porous-zone"

    child_names = \
        ['porous', 'cursys_name', 'dir_spec_cond', 'direction_1_vector',
         'direction_2_vector', 'cone_axis_vector', 'point_on_cone_axis',
         'cone_angle', 'rel_vel_resistance', 'viscous_resistance',
         'alt_inertial_form', 'inertial_resistance', 'power_law_c0',
         'power_law_c1', 'porosity', 'relative_viscosity', 'none', 'corey',
         'stone_1', 'stone_2', 'rel_perm_limit_p1', 'rel_perm_limit_p2',
         'ref_perm_p1', 'exp_p1', 'res_sat_p1', 'ref_perm_p2', 'exp_p2',
         'res_sat_p2', 'ref_perm_p3', 'exp_p3', 'res_sat_p3',
         'capillary_pressure', 'max_capillary_pressure', 'van_genuchten_pg',
         'van_genuchten_ng', 'skjaeveland_nw_pc_coef',
         'skjaeveland_nw_pc_pwr', 'skjaeveland_wet_pc_coef',
         'skjaeveland_wet_pc_pwr', 'brooks_corey_pe', 'brooks_corey_ng',
         'leverett_con_ang', 'rp_cbox_p1', 'rp_edit_p1',
         'rel_perm_tabular_p1', 'rel_perm_table_p1', 'rel_perm_satw_p1',
         'rel_perm_rp_p1', 'rp_cbox_p2', 'rp_edit_p2', 'rel_perm_tabular_p2',
         'rel_perm_table_p2', 'rel_perm_satw_p2', 'rel_perm_rp_p2',
         'wetting_phase', 'non_wetting_phase', 'equib_thermal',
         'non_equib_thermal', 'solid_material', 'area_density',
         'heat_transfer_coeff', 'porous_structure', 'structure_material',
         'anisotropic_spe_diff', 'spe_diff_xx', 'spe_diff_xy', 'spe_diff_xz',
         'spe_diff_yx', 'spe_diff_yy', 'spe_diff_yz', 'spe_diff_zx',
         'spe_diff_zy', 'spe_diff_zz']

    _child_classes = dict(
        porous=porous_cls,
        cursys_name=cursys_name_cls,
        dir_spec_cond=dir_spec_cond_cls,
        direction_1_vector=direction_1_vector_cls,
        direction_2_vector=direction_2_vector_cls,
        cone_axis_vector=cone_axis_vector_cls,
        point_on_cone_axis=point_on_cone_axis_cls,
        cone_angle=cone_angle_cls,
        rel_vel_resistance=rel_vel_resistance_cls,
        viscous_resistance=viscous_resistance_cls,
        alt_inertial_form=alt_inertial_form_cls,
        inertial_resistance=inertial_resistance_cls,
        power_law_c0=power_law_c0_cls,
        power_law_c1=power_law_c1_cls,
        porosity=porosity_cls,
        relative_viscosity=relative_viscosity_cls,
        none=none_cls,
        corey=corey_cls,
        stone_1=stone_1_cls,
        stone_2=stone_2_cls,
        rel_perm_limit_p1=rel_perm_limit_p1_cls,
        rel_perm_limit_p2=rel_perm_limit_p2_cls,
        ref_perm_p1=ref_perm_p1_cls,
        exp_p1=exp_p1_cls,
        res_sat_p1=res_sat_p1_cls,
        ref_perm_p2=ref_perm_p2_cls,
        exp_p2=exp_p2_cls,
        res_sat_p2=res_sat_p2_cls,
        ref_perm_p3=ref_perm_p3_cls,
        exp_p3=exp_p3_cls,
        res_sat_p3=res_sat_p3_cls,
        capillary_pressure=capillary_pressure_cls,
        max_capillary_pressure=max_capillary_pressure_cls,
        van_genuchten_pg=van_genuchten_pg_cls,
        van_genuchten_ng=van_genuchten_ng_cls,
        skjaeveland_nw_pc_coef=skjaeveland_nw_pc_coef_cls,
        skjaeveland_nw_pc_pwr=skjaeveland_nw_pc_pwr_cls,
        skjaeveland_wet_pc_coef=skjaeveland_wet_pc_coef_cls,
        skjaeveland_wet_pc_pwr=skjaeveland_wet_pc_pwr_cls,
        brooks_corey_pe=brooks_corey_pe_cls,
        brooks_corey_ng=brooks_corey_ng_cls,
        leverett_con_ang=leverett_con_ang_cls,
        rp_cbox_p1=rp_cbox_p1_cls,
        rp_edit_p1=rp_edit_p1_cls,
        rel_perm_tabular_p1=rel_perm_tabular_p1_cls,
        rel_perm_table_p1=rel_perm_table_p1_cls,
        rel_perm_satw_p1=rel_perm_satw_p1_cls,
        rel_perm_rp_p1=rel_perm_rp_p1_cls,
        rp_cbox_p2=rp_cbox_p2_cls,
        rp_edit_p2=rp_edit_p2_cls,
        rel_perm_tabular_p2=rel_perm_tabular_p2_cls,
        rel_perm_table_p2=rel_perm_table_p2_cls,
        rel_perm_satw_p2=rel_perm_satw_p2_cls,
        rel_perm_rp_p2=rel_perm_rp_p2_cls,
        wetting_phase=wetting_phase_cls,
        non_wetting_phase=non_wetting_phase_cls,
        equib_thermal=equib_thermal_cls,
        non_equib_thermal=non_equib_thermal_cls,
        solid_material=solid_material_cls,
        area_density=area_density_cls,
        heat_transfer_coeff=heat_transfer_coeff_cls,
        porous_structure=porous_structure_cls,
        structure_material=structure_material_cls,
        anisotropic_spe_diff=anisotropic_spe_diff_cls,
        spe_diff_xx=spe_diff_xx_cls,
        spe_diff_xy=spe_diff_xy_cls,
        spe_diff_xz=spe_diff_xz_cls,
        spe_diff_yx=spe_diff_yx_cls,
        spe_diff_yy=spe_diff_yy_cls,
        spe_diff_yz=spe_diff_yz_cls,
        spe_diff_zx=spe_diff_zx_cls,
        spe_diff_zy=spe_diff_zy_cls,
        spe_diff_zz=spe_diff_zz_cls,
    )

