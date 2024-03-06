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
from .anode_jea import anode_jea as anode_jea_cls
from .anode_cref import anode_cref as anode_cref_cls
from .anode_exp import anode_exp as anode_exp_cls
from .anode_ex_a import anode_ex_a as anode_ex_a_cls
from .anode_ex_c import anode_ex_c as anode_ex_c_cls
from .cathode_jref import cathode_jref as cathode_jref_cls
from .cathode_jea import cathode_jea as cathode_jea_cls
from .cathode_cref import cathode_cref as cathode_cref_cls
from .cathode_exp import cathode_exp as cathode_exp_cls
from .cathode_ex_a import cathode_ex_a as cathode_ex_a_cls
from .cathode_ex_c import cathode_ex_c as cathode_ex_c_cls
from .anode_stde import anode_stde as anode_stde_cls
from .cathode_stde import cathode_stde as cathode_stde_cls
from .std_tem import std_tem as std_tem_cls
from .std_pre import std_pre as std_pre_cls
from .open_voltage import open_voltage as open_voltage_cls
from .anode_entro import anode_entro as anode_entro_cls
from .cathode_entro import cathode_entro as cathode_entro_cls
from .evaporation_rate import evaporation_rate as evaporation_rate_cls
from .condensation_rate import condensation_rate as condensation_rate_cls
from .osmoticdrag_coeff import osmoticdrag_coeff as osmoticdrag_coeff_cls
class parameters(Group):
    """
    Model parameters.
    """

    fluent_name = "parameters"

    child_names = \
        ['anode_jref', 'anode_jea', 'anode_cref', 'anode_exp', 'anode_ex_a',
         'anode_ex_c', 'cathode_jref', 'cathode_jea', 'cathode_cref',
         'cathode_exp', 'cathode_ex_a', 'cathode_ex_c', 'anode_stde',
         'cathode_stde', 'std_tem', 'std_pre', 'open_voltage', 'anode_entro',
         'cathode_entro', 'evaporation_rate', 'condensation_rate',
         'osmoticdrag_coeff']

    _child_classes = dict(
        anode_jref=anode_jref_cls,
        anode_jea=anode_jea_cls,
        anode_cref=anode_cref_cls,
        anode_exp=anode_exp_cls,
        anode_ex_a=anode_ex_a_cls,
        anode_ex_c=anode_ex_c_cls,
        cathode_jref=cathode_jref_cls,
        cathode_jea=cathode_jea_cls,
        cathode_cref=cathode_cref_cls,
        cathode_exp=cathode_exp_cls,
        cathode_ex_a=cathode_ex_a_cls,
        cathode_ex_c=cathode_ex_c_cls,
        anode_stde=anode_stde_cls,
        cathode_stde=cathode_stde_cls,
        std_tem=std_tem_cls,
        std_pre=std_pre_cls,
        open_voltage=open_voltage_cls,
        anode_entro=anode_entro_cls,
        cathode_entro=cathode_entro_cls,
        evaporation_rate=evaporation_rate_cls,
        condensation_rate=condensation_rate_cls,
        osmoticdrag_coeff=osmoticdrag_coeff_cls,
    )

