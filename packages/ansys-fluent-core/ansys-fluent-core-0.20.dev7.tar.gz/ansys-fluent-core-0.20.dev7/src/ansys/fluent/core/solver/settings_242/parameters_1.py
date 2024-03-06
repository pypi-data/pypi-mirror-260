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

from .anode_jref import anode_jref as anode_jref_cls
from .anode_cref import anode_cref as anode_cref_cls
from .anode_exp import anode_exp as anode_exp_cls
from .anode_ex_a import anode_ex_a as anode_ex_a_cls
from .anode_ex_c import anode_ex_c as anode_ex_c_cls
from .cathode_jref import cathode_jref as cathode_jref_cls
from .cathode_cref import cathode_cref as cathode_cref_cls
from .cathode_exp import cathode_exp as cathode_exp_cls
from .cathode_ex_a import cathode_ex_a as cathode_ex_a_cls
from .cathode_ex_c import cathode_ex_c as cathode_ex_c_cls
from .leak_current import leak_current as leak_current_cls
from .anode_stde import anode_stde as anode_stde_cls
from .cathode_stde import cathode_stde as cathode_stde_cls
from .std_temp import std_temp as std_temp_cls
from .std_pre import std_pre as std_pre_cls
from .open_voltage import open_voltage as open_voltage_cls
from .anode_entro import anode_entro as anode_entro_cls
from .cathode_entro import cathode_entro as cathode_entro_cls
from .h2_diff import h2_diff as h2_diff_cls
from .o2_diff import o2_diff as o2_diff_cls
from .h2o_diff import h2o_diff as h2o_diff_cls
from .other_diff import other_diff as other_diff_cls
from .gas_diff_exp import gas_diff_exp as gas_diff_exp_cls
from .transfer_currrent_exp import transfer_currrent_exp as transfer_currrent_exp_cls
from .rk_exp import rk_exp as rk_exp_cls
from .liquid_cov_exp import liquid_cov_exp as liquid_cov_exp_cls
from .liquid_diss_const import liquid_diss_const as liquid_diss_const_cls
from .liquid_rho import liquid_rho as liquid_rho_cls
from .liquid_k import liquid_k as liquid_k_cls
from .upper_liq_pre import upper_liq_pre as upper_liq_pre_cls
from .lower_liq_pre import lower_liq_pre as lower_liq_pre_cls
from .liq_diff import liq_diff as liq_diff_cls
from .velocity_ratio import velocity_ratio as velocity_ratio_cls
from .gas_diss_const import gas_diss_const as gas_diss_const_cls
from .osmotic_coeff import osmotic_coeff as osmotic_coeff_cls
from .lam_a1 import lam_a1 as lam_a1_cls
from .lam_s1 import lam_s1 as lam_s1_cls
from .n2_cross_coeff import n2_cross_coeff as n2_cross_coeff_cls
from .desublimation_rate import desublimation_rate as desublimation_rate_cls
from .sublimation_rate import sublimation_rate as sublimation_rate_cls
class parameters(Group):
    """
    Model parameters.
    """

    fluent_name = "parameters"

    child_names = \
        ['anode_jref', 'anode_cref', 'anode_exp', 'anode_ex_a', 'anode_ex_c',
         'cathode_jref', 'cathode_cref', 'cathode_exp', 'cathode_ex_a',
         'cathode_ex_c', 'leak_current', 'anode_stde', 'cathode_stde',
         'std_temp', 'std_pre', 'open_voltage', 'anode_entro',
         'cathode_entro', 'h2_diff', 'o2_diff', 'h2o_diff', 'other_diff',
         'gas_diff_exp', 'transfer_currrent_exp', 'rk_exp', 'liquid_cov_exp',
         'liquid_diss_const', 'liquid_rho', 'liquid_k', 'upper_liq_pre',
         'lower_liq_pre', 'liq_diff', 'velocity_ratio', 'gas_diss_const',
         'osmotic_coeff', 'lam_a1', 'lam_s1', 'n2_cross_coeff',
         'desublimation_rate', 'sublimation_rate']

    _child_classes = dict(
        anode_jref=anode_jref_cls,
        anode_cref=anode_cref_cls,
        anode_exp=anode_exp_cls,
        anode_ex_a=anode_ex_a_cls,
        anode_ex_c=anode_ex_c_cls,
        cathode_jref=cathode_jref_cls,
        cathode_cref=cathode_cref_cls,
        cathode_exp=cathode_exp_cls,
        cathode_ex_a=cathode_ex_a_cls,
        cathode_ex_c=cathode_ex_c_cls,
        leak_current=leak_current_cls,
        anode_stde=anode_stde_cls,
        cathode_stde=cathode_stde_cls,
        std_temp=std_temp_cls,
        std_pre=std_pre_cls,
        open_voltage=open_voltage_cls,
        anode_entro=anode_entro_cls,
        cathode_entro=cathode_entro_cls,
        h2_diff=h2_diff_cls,
        o2_diff=o2_diff_cls,
        h2o_diff=h2o_diff_cls,
        other_diff=other_diff_cls,
        gas_diff_exp=gas_diff_exp_cls,
        transfer_currrent_exp=transfer_currrent_exp_cls,
        rk_exp=rk_exp_cls,
        liquid_cov_exp=liquid_cov_exp_cls,
        liquid_diss_const=liquid_diss_const_cls,
        liquid_rho=liquid_rho_cls,
        liquid_k=liquid_k_cls,
        upper_liq_pre=upper_liq_pre_cls,
        lower_liq_pre=lower_liq_pre_cls,
        liq_diff=liq_diff_cls,
        velocity_ratio=velocity_ratio_cls,
        gas_diss_const=gas_diss_const_cls,
        osmotic_coeff=osmotic_coeff_cls,
        lam_a1=lam_a1_cls,
        lam_s1=lam_s1_cls,
        n2_cross_coeff=n2_cross_coeff_cls,
        desublimation_rate=desublimation_rate_cls,
        sublimation_rate=sublimation_rate_cls,
    )

