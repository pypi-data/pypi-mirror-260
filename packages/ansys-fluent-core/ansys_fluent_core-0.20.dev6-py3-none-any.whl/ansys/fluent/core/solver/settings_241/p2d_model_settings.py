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

from .initial_soc import initial_soc as initial_soc_cls
from .ref_capacity import ref_capacity as ref_capacity_cls
from .anode_thickness import anode_thickness as anode_thickness_cls
from .anode_n_grid import anode_n_grid as anode_n_grid_cls
from .anode_size_ratio import anode_size_ratio as anode_size_ratio_cls
from .anode_p_diameter import anode_p_diameter as anode_p_diameter_cls
from .anode_n_sphere import anode_n_sphere as anode_n_sphere_cls
from .anode_size_ratio_r import anode_size_ratio_r as anode_size_ratio_r_cls
from .anode_cs_max import anode_cs_max as anode_cs_max_cls
from .anode_stio_0 import anode_stio_0 as anode_stio_0_cls
from .anode_stio_100 import anode_stio_100 as anode_stio_100_cls
from .anode_ce_0 import anode_ce_0 as anode_ce_0_cls
from .anode_vof import anode_vof as anode_vof_cls
from .anode_filler_f import anode_filler_f as anode_filler_f_cls
from .anode_ds import anode_ds as anode_ds_cls
from .anode_ed import anode_ed as anode_ed_cls
from .anode_brugg import anode_brugg as anode_brugg_cls
from .anode_sigma import anode_sigma as anode_sigma_cls
from .anode_i0_1 import anode_i0 as anode_i0_cls
from .anode_er import anode_er as anode_er_cls
from .anode_alpha_a_1 import anode_alpha_a as anode_alpha_a_cls
from .anode_alpha_c_1 import anode_alpha_c as anode_alpha_c_cls
from .anode_ocv import anode_ocv as anode_ocv_cls
from .cathode_thickness import cathode_thickness as cathode_thickness_cls
from .cathode_n_grid import cathode_n_grid as cathode_n_grid_cls
from .cathode_size_ratio import cathode_size_ratio as cathode_size_ratio_cls
from .cathode_p_diameter import cathode_p_diameter as cathode_p_diameter_cls
from .cathode_n_sphere import cathode_n_sphere as cathode_n_sphere_cls
from .cathode_size_ratio_r import cathode_size_ratio_r as cathode_size_ratio_r_cls
from .cathode_cs_max import cathode_cs_max as cathode_cs_max_cls
from .cathode_stio_0 import cathode_stio_0 as cathode_stio_0_cls
from .cathode_stio_100 import cathode_stio_100 as cathode_stio_100_cls
from .cathode_ce_0 import cathode_ce_0 as cathode_ce_0_cls
from .cathode_vof import cathode_vof as cathode_vof_cls
from .cathode_filler_f import cathode_filler_f as cathode_filler_f_cls
from .cathode_ds import cathode_ds as cathode_ds_cls
from .cathode_ed import cathode_ed as cathode_ed_cls
from .cathode_brugg import cathode_brugg as cathode_brugg_cls
from .cathode_sigma import cathode_sigma as cathode_sigma_cls
from .cathode_i0_1 import cathode_i0 as cathode_i0_cls
from .cathode_er import cathode_er as cathode_er_cls
from .cathode_alpha_a_1 import cathode_alpha_a as cathode_alpha_a_cls
from .cathode_alpha_c_1 import cathode_alpha_c as cathode_alpha_c_cls
from .cathode_ocv import cathode_ocv as cathode_ocv_cls
from .electrolyte_thickness import electrolyte_thickness as electrolyte_thickness_cls
from .electrolyte_n_grid import electrolyte_n_grid as electrolyte_n_grid_cls
from .electrolyte_ce_0 import electrolyte_ce_0 as electrolyte_ce_0_cls
from .electrolyte_vof import electrolyte_vof as electrolyte_vof_cls
from .electrolyte_brugg import electrolyte_brugg as electrolyte_brugg_cls
from .electrolyte_de import electrolyte_de as electrolyte_de_cls
from .electrolyte_t_plus import electrolyte_t_plus as electrolyte_t_plus_cls
from .electrolyte_sigma import electrolyte_sigma as electrolyte_sigma_cls
from .electrolyte_activity import electrolyte_activity as electrolyte_activity_cls
from .analytical_cs import analytical_cs as analytical_cs_cls
from .analytical_cs_order import analytical_cs_order as analytical_cs_order_cls
from .aging_model_enabled import aging_model_enabled as aging_model_enabled_cls
from .swelling_model_enabled import swelling_model_enabled as swelling_model_enabled_cls
from .swelling_model_parameter import swelling_model_parameter as swelling_model_parameter_cls
class p2d_model_settings(Group):
    """
    'p2d_model_settings' child.
    """

    fluent_name = "p2d-model-settings"

    child_names = \
        ['initial_soc', 'ref_capacity', 'anode_thickness', 'anode_n_grid',
         'anode_size_ratio', 'anode_p_diameter', 'anode_n_sphere',
         'anode_size_ratio_r', 'anode_cs_max', 'anode_stio_0',
         'anode_stio_100', 'anode_ce_0', 'anode_vof', 'anode_filler_f',
         'anode_ds', 'anode_ed', 'anode_brugg', 'anode_sigma', 'anode_i0',
         'anode_er', 'anode_alpha_a', 'anode_alpha_c', 'anode_ocv',
         'cathode_thickness', 'cathode_n_grid', 'cathode_size_ratio',
         'cathode_p_diameter', 'cathode_n_sphere', 'cathode_size_ratio_r',
         'cathode_cs_max', 'cathode_stio_0', 'cathode_stio_100',
         'cathode_ce_0', 'cathode_vof', 'cathode_filler_f', 'cathode_ds',
         'cathode_ed', 'cathode_brugg', 'cathode_sigma', 'cathode_i0',
         'cathode_er', 'cathode_alpha_a', 'cathode_alpha_c', 'cathode_ocv',
         'electrolyte_thickness', 'electrolyte_n_grid', 'electrolyte_ce_0',
         'electrolyte_vof', 'electrolyte_brugg', 'electrolyte_de',
         'electrolyte_t_plus', 'electrolyte_sigma', 'electrolyte_activity',
         'analytical_cs', 'analytical_cs_order', 'aging_model_enabled',
         'swelling_model_enabled', 'swelling_model_parameter']

    _child_classes = dict(
        initial_soc=initial_soc_cls,
        ref_capacity=ref_capacity_cls,
        anode_thickness=anode_thickness_cls,
        anode_n_grid=anode_n_grid_cls,
        anode_size_ratio=anode_size_ratio_cls,
        anode_p_diameter=anode_p_diameter_cls,
        anode_n_sphere=anode_n_sphere_cls,
        anode_size_ratio_r=anode_size_ratio_r_cls,
        anode_cs_max=anode_cs_max_cls,
        anode_stio_0=anode_stio_0_cls,
        anode_stio_100=anode_stio_100_cls,
        anode_ce_0=anode_ce_0_cls,
        anode_vof=anode_vof_cls,
        anode_filler_f=anode_filler_f_cls,
        anode_ds=anode_ds_cls,
        anode_ed=anode_ed_cls,
        anode_brugg=anode_brugg_cls,
        anode_sigma=anode_sigma_cls,
        anode_i0=anode_i0_cls,
        anode_er=anode_er_cls,
        anode_alpha_a=anode_alpha_a_cls,
        anode_alpha_c=anode_alpha_c_cls,
        anode_ocv=anode_ocv_cls,
        cathode_thickness=cathode_thickness_cls,
        cathode_n_grid=cathode_n_grid_cls,
        cathode_size_ratio=cathode_size_ratio_cls,
        cathode_p_diameter=cathode_p_diameter_cls,
        cathode_n_sphere=cathode_n_sphere_cls,
        cathode_size_ratio_r=cathode_size_ratio_r_cls,
        cathode_cs_max=cathode_cs_max_cls,
        cathode_stio_0=cathode_stio_0_cls,
        cathode_stio_100=cathode_stio_100_cls,
        cathode_ce_0=cathode_ce_0_cls,
        cathode_vof=cathode_vof_cls,
        cathode_filler_f=cathode_filler_f_cls,
        cathode_ds=cathode_ds_cls,
        cathode_ed=cathode_ed_cls,
        cathode_brugg=cathode_brugg_cls,
        cathode_sigma=cathode_sigma_cls,
        cathode_i0=cathode_i0_cls,
        cathode_er=cathode_er_cls,
        cathode_alpha_a=cathode_alpha_a_cls,
        cathode_alpha_c=cathode_alpha_c_cls,
        cathode_ocv=cathode_ocv_cls,
        electrolyte_thickness=electrolyte_thickness_cls,
        electrolyte_n_grid=electrolyte_n_grid_cls,
        electrolyte_ce_0=electrolyte_ce_0_cls,
        electrolyte_vof=electrolyte_vof_cls,
        electrolyte_brugg=electrolyte_brugg_cls,
        electrolyte_de=electrolyte_de_cls,
        electrolyte_t_plus=electrolyte_t_plus_cls,
        electrolyte_sigma=electrolyte_sigma_cls,
        electrolyte_activity=electrolyte_activity_cls,
        analytical_cs=analytical_cs_cls,
        analytical_cs_order=analytical_cs_order_cls,
        aging_model_enabled=aging_model_enabled_cls,
        swelling_model_enabled=swelling_model_enabled_cls,
        swelling_model_parameter=swelling_model_parameter_cls,
    )

