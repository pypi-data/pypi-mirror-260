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

from .anode_ca_zone_list import anode_ca_zone_list as anode_ca_zone_list_cls
from .anode_ca_update import anode_ca_update as anode_ca_update_cls
from .anode_ca_material import anode_ca_material as anode_ca_material_cls
from .anode_ca_porosity import anode_ca_porosity as anode_ca_porosity_cls
from .anode_ca_permeability import anode_ca_permeability as anode_ca_permeability_cls
from .anode_ca_sv_ratio import anode_ca_sv_ratio as anode_ca_sv_ratio_cls
from .anode_ca_alpha import anode_ca_alpha as anode_ca_alpha_cls
from .anode_ca_beta import anode_ca_beta as anode_ca_beta_cls
from .anode_ca_ion_vof import anode_ca_ion_vof as anode_ca_ion_vof_cls
from .anode_ca_act import anode_ca_act as anode_ca_act_cls
from .anode_ca_tortuosity import anode_ca_tortuosity as anode_ca_tortuosity_cls
from .anode_ca_jref_act import anode_ca_jref_act as anode_ca_jref_act_cls
from .anode_ca_jref_t import anode_ca_jref_t as anode_ca_jref_t_cls
from .anode_ca_angle import anode_ca_angle as anode_ca_angle_cls
from .anode_ca_angle_hi import anode_ca_angle_hi as anode_ca_angle_hi_cls
from .anode_ca_fraction import anode_ca_fraction as anode_ca_fraction_cls
from .anode_ca_a import anode_ca_a as anode_ca_a_cls
from .anode_ca_b import anode_ca_b as anode_ca_b_cls
from .anode_ca_c import anode_ca_c as anode_ca_c_cls
from .anode_ca_condensation import anode_ca_condensation as anode_ca_condensation_cls
from .anode_ca_evaporation import anode_ca_evaporation as anode_ca_evaporation_cls
from .anode_ca_poresize import anode_ca_poresize as anode_ca_poresize_cls
class anode_ca_zone(Group):
    """
    Set up anode catalyst layer.
    """

    fluent_name = "anode-ca-zone"

    child_names = \
        ['anode_ca_zone_list', 'anode_ca_update', 'anode_ca_material',
         'anode_ca_porosity', 'anode_ca_permeability', 'anode_ca_sv_ratio',
         'anode_ca_alpha', 'anode_ca_beta', 'anode_ca_ion_vof',
         'anode_ca_act', 'anode_ca_tortuosity', 'anode_ca_jref_act',
         'anode_ca_jref_t', 'anode_ca_angle', 'anode_ca_angle_hi',
         'anode_ca_fraction', 'anode_ca_a', 'anode_ca_b', 'anode_ca_c',
         'anode_ca_condensation', 'anode_ca_evaporation',
         'anode_ca_poresize']

    _child_classes = dict(
        anode_ca_zone_list=anode_ca_zone_list_cls,
        anode_ca_update=anode_ca_update_cls,
        anode_ca_material=anode_ca_material_cls,
        anode_ca_porosity=anode_ca_porosity_cls,
        anode_ca_permeability=anode_ca_permeability_cls,
        anode_ca_sv_ratio=anode_ca_sv_ratio_cls,
        anode_ca_alpha=anode_ca_alpha_cls,
        anode_ca_beta=anode_ca_beta_cls,
        anode_ca_ion_vof=anode_ca_ion_vof_cls,
        anode_ca_act=anode_ca_act_cls,
        anode_ca_tortuosity=anode_ca_tortuosity_cls,
        anode_ca_jref_act=anode_ca_jref_act_cls,
        anode_ca_jref_t=anode_ca_jref_t_cls,
        anode_ca_angle=anode_ca_angle_cls,
        anode_ca_angle_hi=anode_ca_angle_hi_cls,
        anode_ca_fraction=anode_ca_fraction_cls,
        anode_ca_a=anode_ca_a_cls,
        anode_ca_b=anode_ca_b_cls,
        anode_ca_c=anode_ca_c_cls,
        anode_ca_condensation=anode_ca_condensation_cls,
        anode_ca_evaporation=anode_ca_evaporation_cls,
        anode_ca_poresize=anode_ca_poresize_cls,
    )

