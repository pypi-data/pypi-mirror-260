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

from .cathode_ca_zone_list import cathode_ca_zone_list as cathode_ca_zone_list_cls
from .cathode_ca_update import cathode_ca_update as cathode_ca_update_cls
from .cathode_ca_material import cathode_ca_material as cathode_ca_material_cls
from .cathode_ca_porosity import cathode_ca_porosity as cathode_ca_porosity_cls
from .cathode_ca_permeability import cathode_ca_permeability as cathode_ca_permeability_cls
from .cathode_ca_sv_ratio import cathode_ca_sv_ratio as cathode_ca_sv_ratio_cls
from .cathode_ca_alpha import cathode_ca_alpha as cathode_ca_alpha_cls
from .cathode_ca_beta import cathode_ca_beta as cathode_ca_beta_cls
from .cathode_ca_ion_vof import cathode_ca_ion_vof as cathode_ca_ion_vof_cls
from .cathode_ca_act import cathode_ca_act as cathode_ca_act_cls
from .cathode_ca_tortuosity import cathode_ca_tortuosity as cathode_ca_tortuosity_cls
from .cathode_ca_jref_act import cathode_ca_jref_act as cathode_ca_jref_act_cls
from .cathode_ca_jref_t import cathode_ca_jref_t as cathode_ca_jref_t_cls
from .cathode_ca_radius import cathode_ca_radius as cathode_ca_radius_cls
from .cathode_ca_resistance import cathode_ca_resistance as cathode_ca_resistance_cls
from .cathode_ca_kwdw import cathode_ca_kwdw as cathode_ca_kwdw_cls
from .cathode_ca_angle import cathode_ca_angle as cathode_ca_angle_cls
from .cathode_ca_angle_hi import cathode_ca_angle_hi as cathode_ca_angle_hi_cls
from .cathode_ca_fraction import cathode_ca_fraction as cathode_ca_fraction_cls
from .cathode_ca_a import cathode_ca_a as cathode_ca_a_cls
from .cathode_ca_b import cathode_ca_b as cathode_ca_b_cls
from .cathode_ca_c import cathode_ca_c as cathode_ca_c_cls
from .cathode_ca_condensation import cathode_ca_condensation as cathode_ca_condensation_cls
from .cathode_ca_evaporation import cathode_ca_evaporation as cathode_ca_evaporation_cls
from .cathode_ca_poresize import cathode_ca_poresize as cathode_ca_poresize_cls
class cathode_ca_zone(Group):
    """
    Set up cathode catalyst layer.
    """

    fluent_name = "cathode-ca-zone"

    child_names = \
        ['cathode_ca_zone_list', 'cathode_ca_update', 'cathode_ca_material',
         'cathode_ca_porosity', 'cathode_ca_permeability',
         'cathode_ca_sv_ratio', 'cathode_ca_alpha', 'cathode_ca_beta',
         'cathode_ca_ion_vof', 'cathode_ca_act', 'cathode_ca_tortuosity',
         'cathode_ca_jref_act', 'cathode_ca_jref_t', 'cathode_ca_radius',
         'cathode_ca_resistance', 'cathode_ca_kwdw', 'cathode_ca_angle',
         'cathode_ca_angle_hi', 'cathode_ca_fraction', 'cathode_ca_a',
         'cathode_ca_b', 'cathode_ca_c', 'cathode_ca_condensation',
         'cathode_ca_evaporation', 'cathode_ca_poresize']

    _child_classes = dict(
        cathode_ca_zone_list=cathode_ca_zone_list_cls,
        cathode_ca_update=cathode_ca_update_cls,
        cathode_ca_material=cathode_ca_material_cls,
        cathode_ca_porosity=cathode_ca_porosity_cls,
        cathode_ca_permeability=cathode_ca_permeability_cls,
        cathode_ca_sv_ratio=cathode_ca_sv_ratio_cls,
        cathode_ca_alpha=cathode_ca_alpha_cls,
        cathode_ca_beta=cathode_ca_beta_cls,
        cathode_ca_ion_vof=cathode_ca_ion_vof_cls,
        cathode_ca_act=cathode_ca_act_cls,
        cathode_ca_tortuosity=cathode_ca_tortuosity_cls,
        cathode_ca_jref_act=cathode_ca_jref_act_cls,
        cathode_ca_jref_t=cathode_ca_jref_t_cls,
        cathode_ca_radius=cathode_ca_radius_cls,
        cathode_ca_resistance=cathode_ca_resistance_cls,
        cathode_ca_kwdw=cathode_ca_kwdw_cls,
        cathode_ca_angle=cathode_ca_angle_cls,
        cathode_ca_angle_hi=cathode_ca_angle_hi_cls,
        cathode_ca_fraction=cathode_ca_fraction_cls,
        cathode_ca_a=cathode_ca_a_cls,
        cathode_ca_b=cathode_ca_b_cls,
        cathode_ca_c=cathode_ca_c_cls,
        cathode_ca_condensation=cathode_ca_condensation_cls,
        cathode_ca_evaporation=cathode_ca_evaporation_cls,
        cathode_ca_poresize=cathode_ca_poresize_cls,
    )

