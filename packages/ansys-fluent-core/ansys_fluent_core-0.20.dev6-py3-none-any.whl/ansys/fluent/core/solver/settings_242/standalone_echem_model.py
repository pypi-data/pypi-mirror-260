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

from .enabled_24 import enabled as enabled_cls
from .life_model_enabled import life_model_enabled as life_model_enabled_cls
from .report_time_step import report_time_step as report_time_step_cls
from .total_run_num_cycles import total_run_num_cycles as total_run_num_cycles_cls
from .total_run_time import total_run_time as total_run_time_cls
from .ref_temp import ref_temp as ref_temp_cls
from .load_type import load_type as load_type_cls
from .external_p import external_p as external_p_cls
from .total_deformation import total_deformation as total_deformation_cls
from .external_stiff import external_stiff as external_stiff_cls
from .ce_ec import ce_ec as ce_ec_cls
from .diff_ec import diff_ec as diff_ec_cls
from .rho_sei import rho_sei as rho_sei_cls
from .m_sei_1 import m_sei as m_sei_cls
from .kappa_sei import kappa_sei as kappa_sei_cls
from .k0_sei import k0_sei as k0_sei_cls
from .ac_sei import ac_sei as ac_sei_cls
from .u_sei import u_sei as u_sei_cls
from .lithium_plating_enabled import lithium_plating_enabled as lithium_plating_enabled_cls
from .rho_li import rho_li as rho_li_cls
from .m_li import m_li as m_li_cls
from .i0_lpl import i0_lpl as i0_lpl_cls
from .ac_lpl import ac_lpl as ac_lpl_cls
from .u_lpl import u_lpl as u_lpl_cls
from .beta import beta as beta_cls
from .multiplier import multiplier as multiplier_cls
from .save_interval import save_interval as save_interval_cls
from .restart_enabled import restart_enabled as restart_enabled_cls
from .restart_filename import restart_filename as restart_filename_cls
from .restart_profile import restart_profile as restart_profile_cls
from .run_echem_standalone import run_echem_standalone as run_echem_standalone_cls
class standalone_echem_model(Group):
    """
    Run standalone echem model.
    """

    fluent_name = "standalone-echem-model"

    child_names = \
        ['enabled', 'life_model_enabled', 'report_time_step',
         'total_run_num_cycles', 'total_run_time', 'ref_temp', 'load_type',
         'external_p', 'total_deformation', 'external_stiff', 'ce_ec',
         'diff_ec', 'rho_sei', 'm_sei', 'kappa_sei', 'k0_sei', 'ac_sei',
         'u_sei', 'lithium_plating_enabled', 'rho_li', 'm_li', 'i0_lpl',
         'ac_lpl', 'u_lpl', 'beta', 'multiplier', 'save_interval',
         'restart_enabled', 'restart_filename', 'restart_profile']

    command_names = \
        ['run_echem_standalone']

    _child_classes = dict(
        enabled=enabled_cls,
        life_model_enabled=life_model_enabled_cls,
        report_time_step=report_time_step_cls,
        total_run_num_cycles=total_run_num_cycles_cls,
        total_run_time=total_run_time_cls,
        ref_temp=ref_temp_cls,
        load_type=load_type_cls,
        external_p=external_p_cls,
        total_deformation=total_deformation_cls,
        external_stiff=external_stiff_cls,
        ce_ec=ce_ec_cls,
        diff_ec=diff_ec_cls,
        rho_sei=rho_sei_cls,
        m_sei=m_sei_cls,
        kappa_sei=kappa_sei_cls,
        k0_sei=k0_sei_cls,
        ac_sei=ac_sei_cls,
        u_sei=u_sei_cls,
        lithium_plating_enabled=lithium_plating_enabled_cls,
        rho_li=rho_li_cls,
        m_li=m_li_cls,
        i0_lpl=i0_lpl_cls,
        ac_lpl=ac_lpl_cls,
        u_lpl=u_lpl_cls,
        beta=beta_cls,
        multiplier=multiplier_cls,
        save_interval=save_interval_cls,
        restart_enabled=restart_enabled_cls,
        restart_filename=restart_filename_cls,
        restart_profile=restart_profile_cls,
        run_echem_standalone=run_echem_standalone_cls,
    )

